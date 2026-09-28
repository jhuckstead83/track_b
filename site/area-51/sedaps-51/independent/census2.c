/* SEDAPS capture rule: complete state census for a deck of n distinct cards (0..n-1, larger wins).
   Usage: census2 n Q [live3]
     Q=3        : every arrangement of the n cards into three ordered queues (empty queues allowed).
     Q=3 live3  : only states with all three queues nonempty; leaving that set counts as an exit.
     Q=2        : two nonempty queues (War, winner's card placed first); an emptied queue ends play.
   Rule: every nonempty queue plays its front card; the highest card wins; the winner appends
   the played cards in seat order starting from itself (w, w+1, ... mod Q, nonempty seats only).
   Memory: two bits per state (0 unvisited, 1 on the current path, 2 ends/exits, 3 cycles).
   Output: one JSON line with counts and every cycle as [length, live-seat mask, mask varies]. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int n, Q, live3;
static uint64_t ncomp, nstates, fact[21];
static int comp_len[200][3], comp_id[16][16][16];
static uint8_t *col;
static inline int getc2(uint64_t i) { return (col[i >> 2] >> ((i & 3) * 2)) & 3; }
static inline void setc2(uint64_t i, int v) { uint8_t *p = &col[i >> 2]; int sh = (i & 3) * 2; *p = (uint8_t)((*p & ~(3 << sh)) | (v << sh)); }

typedef struct { int len[3]; int q[3][16]; } St;
static uint64_t perm_rank(const int *p) {
  uint64_t r = 0; int used = 0;
  for (int i = 0; i < n; i++) { int less = __builtin_popcount(used & ((1 << p[i]) - 1)); r += (uint64_t)(p[i] - less) * fact[n - 1 - i]; used |= 1 << p[i]; }
  return r;
}
static void perm_unrank(uint64_t r, int *p) {
  int avail[16]; for (int c = 0; c < n; c++) avail[c] = c;
  for (int i = 0; i < n; i++) { uint64_t f = fact[n - 1 - i]; int d = (int)(r / f); r %= f; p[i] = avail[d]; memmove(avail + d, avail + d + 1, sizeof(int) * (n - 1 - i - d)); }
}
static void decode(uint64_t idx, St *s) {
  int p[16]; uint64_t ci = idx % ncomp; perm_unrank(idx / ncomp, p);
  int k = 0; for (int i = 0; i < 3; i++) { s->len[i] = comp_len[ci][i]; for (int j = 0; j < s->len[i]; j++) s->q[i][j] = p[k++]; }
}
/* returns UINT64_MAX when the state lies outside the enumerated set */
static uint64_t encode(const St *s) {
  int p[16], k = 0; for (int i = 0; i < 3; i++) for (int j = 0; j < s->len[i]; j++) p[k++] = s->q[i][j];
  int ci = comp_id[s->len[0]][s->len[1]][s->len[2]];
  if (ci < 0) return UINT64_MAX;
  return perm_rank(p) * ncomp + (uint64_t)ci;
}
static int mask_of(const St *s) { int m = 0; for (int i = 0; i < Q; i++) if (s->len[i]) m |= 1 << i; return m; }
static int step(const St *s, St *t) {       /* 0: terminal (fewer than two live queues) */
  if (__builtin_popcount(mask_of(s)) < 2) return 0;
  int card[3] = {-1, -1, -1}, w = -1; *t = *s;
  for (int i = 0; i < Q; i++) if (s->len[i]) { card[i] = s->q[i][0]; memmove(t->q[i], t->q[i] + 1, sizeof(int) * (t->len[i] - 1)); t->len[i]--; if (w < 0 || card[i] > card[w]) w = i; }
  for (int o = 0; o < Q; o++) { int i = (w + o) % Q; if (card[i] >= 0) t->q[w][t->len[w]++] = card[i]; }
  return 1;
}
static uint64_t next_of(uint64_t x) { St s, t; decode(x, &s); if (!step(&s, &t)) return UINT64_MAX; return encode(&t); }

int main(int argc, char **argv) {
  n = atoi(argv[1]); Q = atoi(argv[2]); live3 = argc > 3 && !strcmp(argv[3], "live3");
  fact[0] = 1; for (int i = 1; i < 21; i++) fact[i] = fact[i - 1] * i;
  memset(comp_id, -1, sizeof comp_id); ncomp = 0;
  for (int a = 0; a <= n; a++) for (int b = 0; a + b <= n; b++) {
    int c = n - a - b;
    if (Q == 2 && (c != 0 || a == 0 || b == 0)) continue;
    if (Q == 3 && live3 && (a == 0 || b == 0 || c == 0)) continue;
    comp_len[ncomp][0] = a; comp_len[ncomp][1] = b; comp_len[ncomp][2] = c; comp_id[a][b][c] = (int)ncomp++;
  }
  nstates = fact[n] * ncomp;
  col = calloc((nstates + 3) / 4, 1);
  if (!col) { fprintf(stderr, "out of memory\n"); return 1; }
  size_t cap = 1 << 12, nc = 0; uint64_t *clen = malloc(cap * 8); int *cmask = malloc(cap * sizeof(int)), *cvar = malloc(cap * sizeof(int));
  uint64_t ends = 0, cyc = 0;
  for (uint64_t i = 0; i < nstates; i++) {
    if (getc2(i)) continue;
    uint64_t x = i; int outcome;
    for (;;) {
      setc2(x, 1);
      uint64_t y = next_of(x);
      if (y == UINT64_MAX) { outcome = 2; break; }
      int c = getc2(y);
      if (c == 1) {                           /* a new cycle through y */
        uint64_t z = y, L = 0; int m = 0, first = -1, var = 0; St u;
        do { decode(z, &u); int mm = mask_of(&u); if (first < 0) first = mm; else if (mm != first) var = 1; m |= mm; z = next_of(z); L++; } while (z != y);
        if (nc == cap) { cap *= 2; clen = realloc(clen, cap * 8); cmask = realloc(cmask, cap * sizeof(int)); cvar = realloc(cvar, cap * sizeof(int)); }
        clen[nc] = L; cmask[nc] = m; cvar[nc] = var; nc++; outcome = 3; break;
      }
      if (c >= 2) { outcome = c; break; }
      x = y;
    }
    /* recolor the path from i until the first state no longer marked 1 */
    for (uint64_t z = i; z != UINT64_MAX && getc2(z) == 1; z = next_of(z)) { setc2(z, outcome); if (outcome == 2) ends++; else cyc++; }
  }
  printf("{\"n\":%d,\"queues\":%d,\"subset\":\"%s\",\"states\":%llu,\"statesThatEndOrExit\":%llu,\"statesThatCycle\":%llu,\"cycles\":%zu,\"cycleList\":[",
         n, Q, Q == 2 ? "both nonempty" : live3 ? "all three nonempty" : "all", (unsigned long long)nstates, (unsigned long long)ends, (unsigned long long)cyc, nc);
  for (size_t k = 0; k < nc; k++) printf("%s[%llu,%d,%d]", k ? "," : "", (unsigned long long)clen[k], cmask[k], cvar[k]);
  printf("]}\n");
  return 0;
}
