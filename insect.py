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


def ComputeLevel(sol, pack):
  cand = pack.remainings()
  if len(sol) > 2:
    up = sol[-3].lst[2]
    cand = (p for p in cand if up + p.lst[0] == 0)
  if len(sol) % 3:
    left = sol[-1].lst[1]
    cand = [p for p in cand if left + p.lst[3] == 0]
  return list(pack.GenCopies(cand, sol))


def Recursive(sol_packs):
  for pairs in sol_packs:
    next_pairs = (ComputeLevel(sol, pack) for sol, pack in pairs)
    next_pairs = [s for s in next_pairs if s]

    if next_pairs:
      if len(next_pairs[0][0][0]) == 9:
        CheckSolution(next_pairs[0][0][0])
      Recursive(next_pairs)


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


def Try():
  Recursive([ComputeLevel([], AllPermutations())])


def CheckSolution(sol):
  for _ in xrange(len(sol), 9):
    sol.append(Piece([0,0,0,0]))
  print Game(sol)

Try()

