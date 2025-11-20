from collections import defaultdict

class Node:
  def __init__(self):
    self.ch = {}   # dict: char -> Node
    self.cnt = 0   # number of words passing through


BRANCH_THRESHOLD = 15


def insert_word(root, w: str):
  n = root
  n.cnt += 1
  for c in w:
    if c not in n.ch:
      n.ch[c] = Node() #for each char create child if missing
    n = n.ch[c]
    n.cnt += 1 #move to child; increment count


def best_split(root, w: str):
  #Returns: (best_index, score, support_count)
  n = root
  best_i = -1 #split index in word
  best_score = 0.0 #how strong the split is
  best_support = 0 #how many words go through this node

  for i, c in enumerate(w):
    if c not in n.ch:
      break
    n = n.ch[c]

    branching = len(n.ch) #different continuations from this node
    if branching < BRANCH_THRESHOLD:
      continue

    max_child = max((child.cnt for child in n.ch.values()), default=0)
    if n.cnt <= 0:
      continue
    frac = 1.0 - float(max_child) / float(n.cnt)
    score = frac * branching

    if score > best_score + 1e-9 or (abs(score - best_score) < 1e-9 and i > best_i):
      best_i = i
      best_score = score
      best_support = n.cnt

  return best_i, best_score, best_support


def looks_common_suffix(s: str):
  #checks for common suffixes, returns (stem, suffix) or None if not found.
  if len(s) > 3 and s.endswith("ies"):
    return s[:-3] + "y", "ies"
  if len(s) > 2 and s.endswith("es"):
    return s[:-2], "es"
  if len(s) > 1 and s.endswith("s"):
    return s[:-1], "s"
  if len(s) > 3 and s.endswith("ing"):
    return s[:-3], "ing"
  if len(s) > 4 and s.endswith("tion"):
    return s[:-4], "tion"
  return None


def main():
  path = "brown_nouns.txt"
  with open(path, "r") as fin:
    words = [line.strip().lower() for line in fin if line.strip()]

  pref, suf = Node(), Node()
  for w in words:
    insert_word(pref, w)
    r = w[::-1]
    insert_word(suf, r)

  pref_count = suf_count = 0
  pref_score_sum = suf_score_sum = 0.0

  with open("prefix_out.txt", "w") as pref_ofs, open("suffix_out.txt", "w") as suf_ofs:
    for w in words:
      # prefix split
      ip, sp, support_p = best_split(pref, w)
      stem_p, sfx_p = "", ""
      score_p = sp
      support_pref = support_p
      if ip != -1:
        stem_p = w[:ip + 1]
        sfx_p = w[ip + 1:]
        if len(stem_p) < 2 or not sfx_p:
          stem_p, sfx_p = w, ""
          score_p, support_pref = 0, 0

      if sfx_p:
        pref_ofs.write(f"{w}={stem_p}+{sfx_p}  # score={score_p} support={support_pref}\n")
        pref_count += 1
        pref_score_sum += score_p
      else:
        pref_ofs.write(f"{w}={w}+  # nosplit\n")

      # suffix split
      rw = w[::-1]
      ir, sr, support_s = best_split(suf, rw)
      stem_s, sfx_s = "", ""
      score_s = sr
      support_suf = support_s
      if ir != -1:
        rev = rw[:ir + 1]
        sfx_s = rev[::-1]
        stem_s = w[:len(w) - len(sfx_s)]
        if len(stem_s) < 2 or not sfx_s:
            stem_s, sfx_s = w, ""
            score_s, support_suf = 0, 0

      if sfx_s:
        suf_ofs.write(f"{w}={stem_s}+{sfx_s}  # score={score_s} support={support_suf}\n")
        suf_count += 1
        suf_score_sum += score_s
      else:
        suf_ofs.write(f"{w}={w}+  # nosplit\n")

  # Decide winner
  winner = "prefix"
  if suf_count > pref_count or (suf_count == pref_count and suf_score_sum > pref_score_sum):
    winner = "suffix"

  chosen_fname = "prefix_out.txt" if winner == "prefix" else "suffix_out.txt"
  with open(chosen_fname, "r") as chosen_in, open("trie_q1_output.txt", "w") as final_ofs:
    for l in chosen_in:
      final_ofs.write(l)

  print(f"written prefix_out={pref_count} suffix_out={suf_count} winner={winner}", 
  file=sys.stderr)
  #output -> written prefix_out=65308 suffix_out=172649 winner=suffix

if __name__ == "__main__":
  import sys
  main()