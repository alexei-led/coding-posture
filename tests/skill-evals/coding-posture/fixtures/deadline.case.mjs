import assert from "node:assert/strict";
import test from "node:test";
import { isExpired } from "./deadline.mjs";

for (const [name, expiresAt, now, expected] of [
  ["past deadline is expired", 9, 10, true],
  ["deadline equal to now is expired", 10, 10, true],
  ["future deadline is active", 11, 10, false],
]) {
  test(name, () => {
    assert.equal(isExpired(expiresAt, now), expected);
  });
}
