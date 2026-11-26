import Std

/-! Finite algebra and rational sign certificates for the crossing example.
    The coherent-menu and compactness arguments remain in the manuscript. -/
namespace MenuCertificate
open Lean.Grind

def expect {R : Type} [CommRing R] (p a b : R) : R :=
  (1-p)*a + p*b

theorem tiltedExpectation {R : Type} [CommRing R] (p center a b : R) :
    expect (center+p) a b = expect center a b + p*(b-a) := by
  unfold expect
  grind

theorem crossingFormula {R : Type} [CommRing R] (p c : R) :
    expect p c (c-1) = c-p := by
  unfold expect
  grind

theorem crossingSigns (a d : Rat) (hd : 0 < d) :
    0 < expect a (a+d/2) (a+d/2-1) ∧
    expect (a+d) (a+d/2) (a+d/2-1) < 0 := by
  rw [crossingFormula, crossingFormula]
  grind

theorem conflictAddsToZero {R : Type} [CommRing R] (a b : R) :
    (a + (-a), b + (-b)) = (0,0) := by
  apply Prod.ext <;> grind

theorem constantRejection (a : Rat) : expect a (-1) (-1) = -1 := by
  unfold expect
  grind

theorem fixedMenuBoundary :
    0 < expect (1/2 + 1/28 : Rat) (-17/32) (15/32) ∧
    expect (1/2 + 1/32 : Rat) (-17/32) (15/32) = 0 := by
  decide +kernel

#print axioms tiltedExpectation
#print axioms crossingFormula
#print axioms crossingSigns
#print axioms conflictAddsToZero
#print axioms constantRejection
#print axioms fixedMenuBoundary
end MenuCertificate
