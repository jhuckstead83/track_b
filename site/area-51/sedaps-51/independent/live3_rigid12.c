/* live3_rigid12.c: every rigid three-live loop at n = 12, found by head set.
 *
 * A rigid loop is one on which the winning card is always a packet head. By the rigidity theorem
 * (RESEARCH_UPDATE_v0_4_1.md section 2) every state on such a loop at n = 12 has pairwise distinct
 * phases 0, 1, 2 and exactly one whole packet [head, member, member] per queue, with the head set H
 * fixed along the loop. The global maximum 11 is always a head, so H = {11, a, b}.
 *
 * For each of the 55 head sets, this program enumerates all 6 * 3! * 9! = 13,063,680 such states
 * and steps each one while the head wins. The rigid step is injective, so a state either returns
 * to itself (it lies on a rigid loop) or reaches a turn where a member wins. It reports, per head
 * set and in total, the states on rigid loops and the loop lengths. The totals are compared with
 * the unrestricted census in LIVE3_LOOPS_RECEIPT.json (live3_loops.c), which was computed by a
 * different method.
 *
 * Build: cc -O2 -fopenmp -o live3_rigid12 live3_rigid12.c   Run: ./live3_rigid12 > live3_rigid12_receipt.json (about 30 s on 4 cores)
 */
#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define N 12
#define CAP 64
typedef struct { unsigned char c[3][CAP]; int len[3]; } St;

static int step(St *s, unsigned hmask) {           /* 1 if the winning card is a head */
    int f0 = s->c[0][0], f1 = s->c[1][0], f2 = s->c[2][0];
    int w = f0 > f1 ? (f0 > f2 ? 0 : 2) : (f1 > f2 ? 1 : 2);
    int f[3] = {f0, f1, f2};
    if (!((hmask >> f[w]) & 1)) return 0;
    for (int i = 0; i < 3; i++) { memmove(s->c[i], s->c[i] + 1, s->len[i] - 1); s->len[i]--; }
    for (int o = 0; o < 3; o++) s->c[w][s->len[w]++] = f[(w + o) % 3];
    return 1;
}
static int same(const St *a, const St *b) {
    for (int i = 0; i < 3; i++) if (a->len[i] != b->len[i] || memcmp(a->c[i], b->c[i], a->len[i])) return 0;
    return 1;
}
static int next_perm(unsigned char *a, int n) {
    int i = n - 2; while (i >= 0 && a[i] >= a[i + 1]) i--; if (i < 0) return 0;
    int j = n - 1; while (a[j] <= a[i]) j--; unsigned char t = a[i]; a[i] = a[j]; a[j] = t;
    for (int l = i + 1, r = n - 1; l < r; l++, r--) { t = a[l]; a[l] = a[r]; a[r] = t; }
    return 1;
}
static const int PERM3[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};

int main(void) {
    int hs[55][2], nh = 0;
    for (int a = 0; a < 11; a++) for (int b = a + 1; b < 11; b++) { hs[nh][0] = a; hs[nh][1] = b; nh++; }
    static uint64_t onLoop[55], states[55], byLen[55][256];
    #pragma omp parallel for schedule(dynamic)
    for (int h = 0; h < nh; h++) {
        unsigned char H[3] = {(unsigned char)hs[h][0], (unsigned char)hs[h][1], 11}, M[9];
        unsigned hmask = (1u << 11) | (1u << hs[h][0]) | (1u << hs[h][1]);
        int m = 0; for (int c = 0; c < N; c++) if (!((hmask >> c) & 1)) M[m++] = (unsigned char)c;
        for (int ph = 0; ph < 6; ph++)                 /* phase of queue i is PERM3[ph][i] */
        for (int hp = 0; hp < 6; hp++) {               /* head of queue i is H[PERM3[hp][i]] */
            unsigned char mem[9]; memcpy(mem, M, 9);
            do {
                St s0; int k = 0;
                for (int i = 0; i < 3; i++) {
                    int p = PERM3[ph][i], L = 0;
                    for (int t = 0; t < p; t++) s0.c[i][L++] = mem[k++];
                    s0.c[i][L++] = H[PERM3[hp][i]]; s0.c[i][L++] = mem[k++]; s0.c[i][L++] = mem[k++];
                    s0.len[i] = L;
                }
                states[h]++;
                St s = s0; int len = 0;
                while (len < 100000 && step(&s, hmask)) { len++; if (same(&s, &s0)) break; }
                if (len && same(&s, &s0)) { onLoop[h]++; byLen[h][len < 255 ? len : 255]++; }
            } while (next_perm(mem, 9));
        }
    }
    uint64_t tot = 0, totS = 0, tl[256] = {0};
    printf("{\n \"program\": \"live3_rigid12.c\",\n \"n\": 12,\n \"perHeadSet\": [\n");
    int first = 1;
    for (int h = 0; h < nh; h++) {
        tot += onLoop[h]; totS += states[h];
        for (int l = 0; l < 256; l++) tl[l] += byLen[h][l];
        if (!onLoop[h]) continue;
        printf("%s  {\"heads\": [%d, %d, 11], \"statesOnRigidLoops\": %llu, \"loops\": {", first ? "" : ",\n",
               hs[h][0], hs[h][1], (unsigned long long)onLoop[h]);
        int f2 = 1;
        for (int l = 1; l < 256; l++) if (byLen[h][l]) { printf("%s\"%d\": %llu", f2 ? "" : ", ", l, (unsigned long long)(byLen[h][l] / l)); f2 = 0; }
        printf("}}"); first = 0;
    }
    printf("\n ],\n \"statesEnumerated\": %llu,\n \"statesOnRigidLoops\": %llu,\n \"loops\": {", (unsigned long long)totS, (unsigned long long)tot);
    int f3 = 1;
    for (int l = 1; l < 256; l++) if (tl[l]) { printf("%s\"%d\": %llu", f3 ? "" : ", ", l, (unsigned long long)(tl[l] / l)); f3 = 0; }
    printf("}\n}\n");
    return 0;
}
