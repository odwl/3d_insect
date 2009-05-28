#!/usr/bin/python2.5

import itertools


def AllPieces():
  return [Piece([2, -4, -2, 3]), Piece([-1, 2, 3, -4]),
          Piece([-1, -4, -2, -3]), Piece([1, -2, -3, 4]),
          Piece([1, 3, -3, -4]), Piece([1, -1, 4, 2]), Piece([1, -4, 3, 2]),
          Piece([1, 4, 3, -2]), Piece([-1, -4, 3, 2])]

class Piece(object):

  def __init__(self, lst, pos=0):
    self.lst = list(self._Pos(lst, pos))

  def _Pos(self, lst, nb):
    cycle =  itertools.cycle(lst)
    return itertools.islice(cycle, nb, nb + 4)

  def __str__(self):
    inter = ','.join('%s' % l for l in self.lst)
    return 'P[%s]' % inter

  def __repr__(self):
    return str(self)

  def __eq__(self, p):
    return sorted(self.lst) == sorted(p.lst)

# ROUGE 1, VIOLET 2, JAUNE 3, VERT 4

class Game(object):
  """A wraper around a solution.

    Attributes:
      pieces: A list of Pieces of size 9
  """

  def __init__(self, pieces):
    assert len(pieces) == 9
    self.pieces = pieces

  def __str__(self):
    str = ''
    for row in xrange(3):
      for line in xrange(3):
        for col in xrange(3):
          pos = 3 * row + col
          if line == 0:
            str += '  %d  |' % self.pieces[pos].lst[0]
          elif line == 2:
            str += '  %d  |' % self.pieces[pos].lst[2]
          else:
            str += '%d  %d |' % (self.pieces[pos].lst[3],
                                 self.pieces[pos].lst[1])
        str += '\n'
      str += '-------------------\n'
    return str


class AllPermutations(object):
  def __init__(self):
    self.pieces = AllPieces()

  def remainings(self):
    for p in self.pieces:
      for perm in xrange(4):
        yield Piece(p.lst, perm)

  def remove(self, piece):
    self.pieces.remove(piece)

  def copy(self):
    new_pack = AllPermutations()
    new_pack.pieces = self.pieces[:]
    return new_pack

  def GenCopies(self, it, sol):
    for piece in it:
      new_pack = self.copy()
      new_sol = sol[:]
      new_sol.append(piece)
      new_pack.remove(piece)
      yield new_sol, new_pack


def ComputeLevel(candidate):
  """Compute the canditates for the next level.

    Args:
      candidate: A Candidate instance.

    Returns:
      An iterator of Candidates.
  """
  sol = candidate.solution
  pack = candidate.remainings
  cand = pack.remainings()
  if len(sol) > 2:
    up = sol[-3].lst[2]
    cand = (p for p in cand if up + p.lst[0] == 0)
  if len(sol) % 3:
    left = sol[-1].lst[1]
    cand = [p for p in cand if left + p.lst[3] == 0]
  for pair in pack.GenCopies(cand, sol):
    if pair:
      yield Candidate(*pair)


def Recursive(candidates):
  """Recursively select some candidate.

  Arguments:
    candidates: An iterator of Candidate.
  """
  for candidate in candidates:
    new_candidates = list(ComputeLevel(candidate))
    if new_candidates:
      if new_candidates[0].is_complete:
        CheckSolution(new_candidates[0].solution)
      Recursive(new_candidates)


class Candidate(object):
  """A wrapper around a partial solution and remainings pieces.

    Attributes:
      solution: A list of Pieces representing the nth first element of a
        solution candidate.
      remainings: An AllPermutations instance.
  """

  def __init__(self, solution, remainings):
    self.solution = solution
    self.remainings = remainings

  @property
  def is_complete(self):
    return len(self.solution) == 9


def Try():
  inital_candidates = [([], AllPermutations())]
  inital_candidates = [Candidate([], AllPermutations())]
  Recursive(inital_candidates)


def CheckSolution(sol):
  for _ in xrange(len(sol), 9):
    sol.append(Piece([0,0,0,0]))
  print Game(sol)

Try()

