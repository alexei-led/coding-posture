export function isExpired(expiresAt, now) {
  return expiresAt < now;
}
