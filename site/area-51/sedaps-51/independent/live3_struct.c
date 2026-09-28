/* live3_struct.c: the structure of every three-live loop (v0.4.1 section 2).
 *
 * Rule: every live queue plays its front card; the highest card wins; the winner appends the
 * played cards to its own tail in seat order starting from itself (winner's card first).
 *
 * Fact 1: on a loop that keeps three queues live, every state is in PACKET FORM: each queue is a
 *   tail of p <= 2 cards of one packet, followed by whole 3-card packets, each led by its largest
 *   card. (After a full period every queue has replayed its content, so it consists of won packets.)
 * Fact 2: packet form is preserved by a turn as long as all three queues stay live.
 * So a three-live loop exists iff some packet-form state never loses a queue. This program walks
 * every packet-form state of n cards forward until a queue empties, and reports any walk that
 * returns to its start or exceeds the step cap.
 *
 * This variant is live3_loops.c plus, for each loop found, a structural classification: largest
 * queue, whether every win gap is 3, whether the winner always plays a packet head, and whether
 * exactly one queue plays a head on each turn.
 * Usage: live3_struct n [shard nshards]    prints one JSON line; n = 12 in four shards.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 16
#define RB 64
static int n, shard = 0, nshards = 1, congOnly = 0;
static int len[3], part[3];
static int slotRole[MAXN], slotHead[MAXN]; /* role: -1 partial, 0 head, 1/2 member */
static int card[MAXN];
static uint64_t states = 0, steps_total = 0, capped = 0, maxExit = 0;
static const uint64_t CAP = 1u << 24;

typedef struct { int q[3][RB]; int h[3], l[3]; } St;

static int same(const St *a, const St *b) {
  for (int i = 0; i < 3; i++) {
    if (a->l[i] != b->l[i]) return 0;
    for (int k = 0; k < a->l[i]; k++)
      if (a->q[i][(a->h[i] + k) & (RB - 1)] != b->q[i][(b->h[i] + k) & (RB - 1)]) return 0;
  }
  return 1;
}
/* lexicographic order on (lengths, then cards queue by queue) */
static int cmpst(const St *a, const St *b) {
  for (int i = 0; i < 3; i++) if (a->l[i] != b->l[i]) return a->l[i] < b->l[i] ? -1 : 1;
  for (int i = 0; i < 3; i++) for (int k = 0; k < a->l[i]; k++) {
    int x = a->q[i][(a->h[i] + k) & (RB - 1)], y = b->q[i][(b->h[i] + k) & (RB - 1)];
    if (x != y) return x < y ? -1 : 1;
  }
  return 0;
}
static inline int turn(St *s) { /* returns winner, or -1 if a queue empties */
  int f[3], w = 0;
  for (int i = 0; i < 3; i++) f[i] = s->q[i][s->h[i]];
  if (f[1] > f[w]) w = 1;
  if (f[2] > f[w]) w = 2;
  for (int i = 0; i < 3; i++) { s->h[i] = (s->h[i] + 1) & (RB - 1); s->l[i]--; }
  for (int o = 0; o < 3; o++) { int j = (w + o) % 3; s->q[w][(s->h[w] + s->l[w]) & (RB - 1)] = f[j]; s->l[w]++; }
  return (!s->l[0] || !s->l[1] || !s->l[2]) ? -1 : w;
}
static uint64_t onLoop = 0, entersLoop = 0, distinctLoops = 0, lenHist[4096], structStats[16][2][2][2], rotating = 0;
static void printst(FILE *o, const St *s) { for (int i = 0; i < 3; i++) { fprintf(o, " |"); for (int k = 0; k < s->l[i]; k++) fprintf(o, " %d", s->q[i][(s->h[i] + k) & (RB - 1)]); } }
static void walk(void) {
  St s, s0, saved; int pos = 0;
  for (int i = 0; i < 3; i++) { s.h[i] = 0; s.l[i] = len[i]; for (int k = 0; k < len[i]; k++) s.q[i][k] = card[pos++]; }
  s0 = s; saved = s;
  uint64_t t = 0, power = 1;
  for (;;) {
    t++;
    if (turn(&s) < 0) { steps_total += t; if (t > maxExit) maxExit = t; return; }
    if (same(&s, &s0)) { /* start lies on a loop of length t */
      onLoop++; uint64_t L = t; St u = s0; int minimal = 1;
      for (uint64_t k = 1; k < L; k++) { turn(&u); if (cmpst(&u, &s0) < 0) { minimal = 0; break; } }
      if (minimal) { distinctLoops++; lenHist[L < 4095 ? L : 4095]++;
        /* structure of this loop: sizes, win pattern, and whether the winner always plays a packet head */
        St v = s0; int prevw = -1, gapsAll3 = 1, rotDir = 0, headWins = 1, maxLen = 0, oneHead = 1; int lastWin[3] = {-1,-1,-1};
        for (uint64_t k = 0; k < 2 * L; k++) {
          int heads = 0, wHead = 0, f[3], w = 0;
          for (int i = 0; i < 3; i++) { int p = v.l[i] % 3; if (p == 0) heads++; f[i] = v.q[i][v.h[i]]; if (v.l[i] > maxLen) maxLen = v.l[i]; }
          if (f[1] > f[w]) w = 1; if (f[2] > f[w]) w = 2;
          wHead = (v.l[w] % 3 == 0);
          if (heads != 1) oneHead = 0;
          if (!wHead) headWins = 0;
          if (k >= L) { if (lastWin[w] >= 0 && (int)k - lastWin[w] != 3) gapsAll3 = 0; }
          lastWin[w] = (int)k;
          if (prevw >= 0) { int d = (w - prevw + 3) % 3; if (rotDir == 0) rotDir = d; else if (d != rotDir) rotDir = 3; }
          prevw = w; turn(&v);
        }
        structStats[maxLen < 16 ? maxLen : 15][gapsAll3][headWins][oneHead]++;
        if (rotDir == 1 || rotDir == 2) rotating++;
        if (distinctLoops <= 20) { fprintf(stderr, "LOOP n=%d length %llu rep:", n, (unsigned long long)L); printst(stderr, &s0); fprintf(stderr, "\n"); } }
      return;
    }
    if (same(&s, &saved)) { entersLoop++; return; }
    if (t == power) { saved = s; power <<= 1; }
    if (t >= CAP) { capped++; return; }
  }
}
static void fill(int k, uint32_t avail) {
  if (k == n) { states++; walk(); return; }
  int role = slotRole[k];
  for (int c = 0; c < n; c++) {
    if (!(avail >> c & 1)) continue;
    if (role > 0 && c > card[slotHead[k]]) continue; /* members lie below their head */
    card[k] = c; fill(k + 1, avail & ~(1u << c));
  }
}

int main(int argc, char **argv) {
  n = atoi(argv[1]);
  if (argc > 3) { shard = atoi(argv[2]); nshards = atoi(argv[3]); }
  if (argc > 4 && !strcmp(argv[4], "cong")) congOnly = 1; /* only sizes pairwise congruent mod 3 */
  if (n < 3 || n > MAXN) return 1;
  uint64_t patterns = 0, pid = 0;
  for (len[0] = 1; len[0] <= n - 2; len[0]++)
    for (len[1] = 1; len[0] + len[1] <= n - 1; len[1]++) {
      len[2] = n - len[0] - len[1];
      for (part[0] = 0; part[0] <= 2; part[0]++)
        for (part[1] = 0; part[1] <= 2; part[1]++)
          for (part[2] = 0; part[2] <= 2; part[2]++) {
            int ok = 1;
            for (int i = 0; i < 3; i++) if (part[i] > len[i] || (len[i] - part[i]) % 3) ok = 0;
            if (!ok) continue;
            if (congOnly && !(len[0] % 3 == len[1] % 3 && len[1] % 3 == len[2] % 3)) continue;
            if ((pid++ % nshards) != (uint64_t)shard) continue;
            patterns++;
            int pos = 0;
            for (int i = 0; i < 3; i++)
              for (int j = 0; j < len[i]; j++, pos++) {
                if (j < part[i]) { slotRole[pos] = -1; slotHead[pos] = -1; }
                else { int r = (j - part[i]) % 3; slotRole[pos] = r; slotHead[pos] = pos - r; }
              }
            fill(0, (1u << n) - 1);
          }
    }
  printf("{\"n\": %d, \"congruentSizesOnly\": %d, \"shard\": %d, \"nshards\": %d, \"patterns\": %llu, \"packetFormStates\": %llu, \"statesOnThreeLiveLoops\": %llu, \"statesEnteringALoop\": %llu, \"distinctThreeLiveLoops\": %llu, \"capped\": %llu, \"maxStepsToLoseAQueue\": %llu, \"loopLengths\": {",
    n, congOnly, shard, nshards, (unsigned long long)patterns, (unsigned long long)states, (unsigned long long)onLoop, (unsigned long long)entersLoop,
    (unsigned long long)distinctLoops, (unsigned long long)capped, (unsigned long long)maxExit);
  int first = 1; for (int L = 0; L < 4096; L++) if (lenHist[L]) { printf("%s\"%d\": %llu", first ? "" : ", ", L, (unsigned long long)lenHist[L]); first = 0; }
  printf("}, \"rotatingWinners\": %llu, \"structure\": [", (unsigned long long)rotating);
  int fs = 1; for (int m = 0; m < 16; m++) for (int g = 0; g < 2; g++) for (int h = 0; h < 2; h++) for (int o = 0; o < 2; o++) if (structStats[m][g][h][o]) {
    printf("%s{\"maxQueue\": %d, \"allGaps3\": %d, \"winnerAlwaysPlaysHead\": %d, \"exactlyOneHeadPerTurn\": %d, \"loops\": %llu}", fs ? "" : ", ", m, g, h, o, (unsigned long long)structStats[m][g][h][o]); fs = 0; }
  printf("]}\n");
  return 0;
}
