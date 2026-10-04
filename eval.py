# Edit TESTS with your own questions + a keyword that must appear in the top match's item/note.
import core
TESTS = [("where is my wallet?", "wallet"), ("where are my spare keys?", "key"), ("what is the wifi password?", "wifi"),("where are my Carnmax?", "Medicine")]
ok = 0
for q, kw in TESTS:
    _, hits = core.ask(q)
    top = hits[0] if hits else {}
    blob = f"{top.get('item','')} {top.get('user_note','')} {top.get('category','')}".lower()
    good = kw in blob
    ok += good
    print("PASS" if good else "FAIL", q, round(top.get("score", 0), 2))
print(f"Top-1 retrieval accuracy: {ok}/{len(TESTS)} = {ok/len(TESTS):.0%}")
