export const SUITS = Object.freeze(["S", "H", "D", "C"]);
export const RANKS = Object.freeze(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]);
export const SUIT_GLYPH = Object.freeze({S: "♠", H: "♥", D: "♦", C: "♣"});

// Exact published v7.2 order. 2C is the outside marker Ⅰ; the other 51 cards
// are the shared Area 51 laboratory object.
export const PUBLISHED_DECK = Object.freeze([
  "AS", "AH", "AD", "AC", "2S", "2H", "2D", "3S", "3H", "3D", "3C",
  "4S", "4H", "4D", "4C", "5S", "5H", "5D", "5C", "6S", "6H", "6D",
  "6C", "7S", "7H", "7D", "7C", "8S", "8H", "8D", "8C", "9S", "9H",
  "9D", "9C", "QD", "KH", "10H", "KD", "QH", "QS", "JS", "10C", "JC",
  "QC", "KC", "10S", "JD", "JH", "KS", "10D", "2C"
]);

export const MARKER_CARD = "2C";
export const ACTIVE_DECK = Object.freeze(PUBLISHED_DECK.filter(card => card !== MARKER_CARD));

export function rankOf(card) {
  return card.slice(0, -1);
}

export function suitOf(card) {
  return card.slice(-1);
}

export function rankNumber(card) {
  return RANKS.indexOf(rankOf(card)) + 1;
}

export function blackjackValue(card) {
  const rank = rankOf(card);
  if (rank === "A") return 1;
  if (["10", "J", "Q", "K"].includes(rank)) return 10;
  return Number(rank);
}

export function blackjackClass(card) {
  return blackjackValue(card) === 10 ? "T" : rankOf(card);
}

export function isRed(card) {
  return /[HD]$/.test(card);
}

export function face(card) {
  return `${rankOf(card)}${SUIT_GLYPH[suitOf(card)]}`;
}

export function assertActiveDeck(deck) {
  if (!Array.isArray(deck) || deck.length !== 51) throw new Error("The active deck must contain 51 cards.");
  if (new Set(deck).size !== 51) throw new Error("The active deck contains a duplicate card.");
  if (deck.includes(MARKER_CARD)) throw new Error("2C must remain outside the active deck as Ⅰ.");
  for (const card of deck) if (!ACTIVE_DECK.includes(card)) throw new Error(`Unknown active card: ${card}`);
  return true;
}

export function randomInt(maxExclusive) {
  if (!Number.isInteger(maxExclusive) || maxExclusive <= 0) throw new Error("randomInt requires a positive integer bound.");
  if (globalThis.crypto?.getRandomValues) {
    const ceiling = 0x100000000;
    const limit = ceiling - (ceiling % maxExclusive);
    const word = new Uint32Array(1);
    do globalThis.crypto.getRandomValues(word); while (word[0] >= limit);
    return word[0] % maxExclusive;
  }
  return Math.floor(Math.random() * maxExclusive);
}

export function shuffled(deck = ACTIVE_DECK) {
  assertActiveDeck(deck);
  const result = [...deck];
  for (let i = result.length - 1; i > 0; i -= 1) {
    const j = randomInt(i + 1);
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

export function swappedPublishedDeck() {
  const deck = [...ACTIVE_DECK];
  [deck[49], deck[50]] = [deck[50], deck[49]];
  return deck;
}

export function valueProjection(deck) {
  return deck.map(blackjackClass);
}

export function defaultMemoryCard(card) {
  const position = ACTIVE_DECK.indexOf(card) + 1;
  const rank = rankOf(card);
  const suit = suitOf(card);
  const color = isRed(card) ? "red" : "black";
  const value = blackjackValue(card);
  const sentinel = card === "3H" ? " Lucky sentinel; it changes no rule or reward." : "";
  return {
    id: card,
    face: face(card),
    symbol: `V=${value} · R=${rankNumber(card)} · C=${color} · S=${SUIT_GLYPH[suit]}`,
    meaning: `${face(card)} is frozen position ${position} of 51; blackjack class ${blackjackClass(card)}; natural rank ${rank}; ${color} ${SUIT_GLYPH[suit]}.${sentinel}`,
    version: 1
  };
}

export function defaultMemoryDeck() {
  return ACTIVE_DECK.map(defaultMemoryCard);
}
