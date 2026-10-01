"""Anemia — animated explainer (Manim CE, no LaTeX)."""
from manim import *

BG = "#1C1C1C"
RED = "#FF4D4D"
BLUE = "#58C4DD"
GREEN = "#83C167"
GOLD = "#FFD93D"
GREY = "#888888"
MONO = "DejaVu Sans Mono"


def T(text, size=30, color=WHITE, weight=NORMAL):
    return Text(text, font_size=size, color=color, font=MONO, weight=weight)


class S1_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = T("Anemia", 72, RED, BOLD)
        sub = T("a sign, not a diagnosis", 30, GREY).next_to(title, DOWN, buff=0.6)
        ring = Circle(radius=2.2, color=RED, stroke_width=3, stroke_opacity=0.5)
        ring.move_to(title.get_center())
        self.add_subcaption("Anemia: a sign, not a diagnosis.", duration=4)
        self.play(Write(title), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(sub, shift=UP * 0.3), Create(ring), run_time=1.5)
        self.wait(5.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class S2_Oxygen(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = T("Why does low Hb matter?", 36, BLUE, BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=1.0)
        self.wait(0.8)

        # RBC (biconcave suggestion: red disc with lighter center)
        rbc = Circle(radius=1.1, color=RED, fill_color=RED, fill_opacity=0.85, stroke_width=2)
        inner = Circle(radius=0.55, color="#FF8A8A", stroke_width=0,
                       fill_color="#FF8A8A", fill_opacity=0.9)
        rbc_group = VGroup(rbc, inner).move_to(LEFT * 4 + UP * 0.4)
        rbc_label = T("RBC", 24, RED).next_to(rbc_group, DOWN, buff=0.3)
        self.play(GrowFromCenter(rbc_group), run_time=1.2)
        self.play(FadeIn(rbc_label), run_time=0.5)
        self.wait(0.8)

        # Hb dots inside
        hb = VGroup(*[Dot(point=rbc_group.get_center() + RIGHT * dx + UP * dy,
                          radius=0.09, color=GOLD)
                      for dx, dy in [(-0.4, 0.3), (0.4, 0.3), (0, -0.35), (-0.35, -0.2), (0.35, -0.2)]])
        hb_label = T("hemoglobin (Hb)", 24, GOLD).next_to(rbc_label, DOWN, buff=0.35)
        self.play(FadeIn(hb, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(hb_label), run_time=0.6)
        self.wait(1.2)

        # O2 arrows flowing to tissue
        tissue = T("tissues", 30, BLUE, BOLD).move_to(RIGHT * 4.2 + UP * 0.4)
        tissue_box = SurroundingRectangle(tissue, color=BLUE, stroke_width=3, stroke_opacity=0.8, buff=0.3)
        flows = VGroup()
        for dy in (-0.55, 0, 0.55):
            arrow = Arrow(LEFT * 2.4 + UP * 0.4 + UP * dy,
                          RIGHT * 3.3 + UP * 0.4 + UP * dy,
                          color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.15)
            o2 = T("O2", 22, GOLD).scale(0.9).next_to(arrow.get_start(), UP, buff=0.15)
            flows.add(VGroup(arrow, o2))
        self.play(FadeIn(tissue), Create(tissue_box), run_time=0.8)
        self.play(*[FadeIn(f, shift=RIGHT * 0.3) for f in flows], run_time=1.5)
        self.wait(1.5)

        note = T("Each Hb carries O2 -> less O2 delivered", 26, WHITE,
                 ).to_edge(DOWN, buff=0.5)
        self.add_subcaption("Each hemoglobin carries oxygen — less Hb means less oxygen delivered.", duration=3)
        self.play(Write(note), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class S3_Definition(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = T("What counts as anemia?", 36, BLUE, BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=1.0)
        self.wait(0.8)

        lines = VGroup(
            VGroup(T("Adult men", 30, WHITE), T("Hb < 13 g/dL", 34, RED, BOLD)),
            VGroup(T("Non-pregnant women", 30, WHITE), T("Hb < 12 g/dL", 34, RED, BOLD)),
            VGroup(T("Pregnant women", 30, WHITE), T("Hb < 11 g/dL", 34, RED, BOLD)),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(DOWN * 0.4)
        for row in lines:
            y = row.get_center()[1]
            row[0].move_to([-2.5, y, 0])
            row[1].move_to([2.5, y, 0])
            row[0].set_opacity(0.85)
        rules = VGroup(*[Line(LEFT * 5, RIGHT * 5, color=GREY, stroke_width=1,
                              stroke_opacity=0.15).move_to(row.get_center())
                         for row in lines])
        self.add(rules)
        who = T("WHO thresholds", 24, GREY).to_edge(DOWN, buff=0.5).set_opacity(0.6)
        self.add_subcaption("WHO defines anemia as Hb below 13 in men, 12 in women, 11 in pregnancy.", duration=4)
        for row in lines:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.6)
        self.play(FadeIn(who), run_time=0.6)
        self.wait(2.0)

        caveat = T("Thresholds vary: age, altitude, pregnancy", 26, GOLD).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(who, caveat), run_time=1.0)
        self.wait(3.1)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class S4_Mechanisms(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = T("Two ways to get there", 36, GREEN, BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=1.0)
        self.wait(0.8)

        # Center: low Hb state (positioned after lists so arrows anchor correctly)
        left_title = T("Make less", 32, BLUE, BOLD).move_to(LEFT * 4.3 + UP * 1.0)
        left_items = VGroup(T("iron deficiency", 26, WHITE),
                            T("B12 / folate deficiency", 26, WHITE),
                            T("bone marrow failure", 26, WHITE),
                            T("chronic disease (CKD)", 26, WHITE)
                            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        left_items.next_to(left_title, DOWN, buff=0.4)
        left_items.set_opacity(0.85)

        right_title = T("Lose / destroy more", 32, GOLD, BOLD).move_to(RIGHT * 4.2 + UP * 1.0)
        right_items = VGroup(T("bleeding (GI, menses)", 26, WHITE),
                             T("hemolysis", 26, WHITE),
                             T("hypersplenism", 26, WHITE)
                             ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        right_items.next_to(right_title, DOWN, buff=0.4)
        right_items.set_opacity(0.85)

        low = T("LOW Hb", 40, RED, BOLD).move_to(DOWN * 0.6)
        low_box = SurroundingRectangle(low, color=RED, buff=0.3, stroke_width=2)
        arrowL = Arrow(LEFT * 4.3 + UP * 0.4, low_box.get_left() + LEFT * 0.3, color=BLUE, stroke_width=4)
        arrowR = Arrow(RIGHT * 4.2 + UP * 0.4, low_box.get_right() + RIGHT * 0.3, color=GOLD, stroke_width=4)

        self.add_subcaption("Anemia arises from decreased production or increased loss/destruction.", duration=3)
        self.play(FadeIn(left_title, shift=DOWN * 0.2), FadeIn(right_title, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(left_items, lag_ratio=0.2), FadeIn(right_items, lag_ratio=0.2), run_time=1.8)
        self.wait(1.5)
        self.play(Write(low), Create(low_box), GrowFromCenter(arrowL), GrowFromCenter(arrowR), run_time=1.8)
        self.wait(2.5)

        punch = T("Same endpoint - different workup", 28, GREEN).to_edge(DOWN, buff=0.5)
        self.add_subcaption("Same endpoint — different workup.", duration=2)
        self.play(FadeIn(punch, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class S5_MCV(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = T("The practical first step: MCV", 36, GOLD, BOLD).to_edge(UP, buff=0.5)
        mcv_def = T("mean corpuscular volume = size of the red cell", 22, GREY).next_to(header, DOWN, buff=0.25)
        mcv_def.set_opacity(0.6)
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=1.0)
        self.play(FadeIn(mcv_def), run_time=0.6)
        self.wait(1.0)

        colors = [BLUE, GREEN, RED]
        radii = [0.45, 0.62, 0.85]
        cols = VGroup()
        heads = [("MICROCYTIC", "MCV < 80",
                  ["iron deficiency", "thalassemia", "chronic disease"]),
                 ("NORMOCYTIC", "MCV 80-100",
                  ["acute blood loss", "CKD", "early iron deficiency"]),
                 ("MACROCYTIC", "MCV > 100",
                  ["B12 / folate deficiency", "liver disease", "hypothyroidism"])]
        for (name, rng, items), c, r in zip(heads, colors, radii):
            col = VGroup(T(name, 28, c, BOLD), T(rng, 22, GREY))
            cell = Circle(radius=r, color=c, stroke_width=3, stroke_opacity=0.9)
            col.add(cell)
            col.add(*[T(it, 22, WHITE).set_opacity(0.85) for it in items])
            col.arrange(DOWN, buff=0.28)
            cols.add(col)
        cols.arrange(RIGHT, buff=1.2)
        cols.scale_to_fit_width(11.2)
        top = max(col[0].get_top()[1] for col in cols)
        for col in cols:
            col.shift(UP * (top - col[0].get_top()[1]))
        cols.move_to(UP * 0.3)
        self.add_subcaption("Microcytic, normocytic, macrocytic — the MCV organizes the differential.", duration=4)
        for col in cols:
            self.play(FadeIn(col, shift=UP * 0.2), run_time=1.1)
            self.wait(2.6)
        self.wait(3.0)
        tip = T("next: ferritin, hemolysis screen, B12 - guided by the column", 24, GOLD).to_edge(DOWN, buff=0.5)
        self.add_subcaption("Ferritin, hemolysis screen or B12 next — guided by the column.", duration=3)
        self.play(Write(tip), run_time=1.5)
        self.wait(3.9)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class S6_Close(Scene):
    def construct(self):
        self.camera.background_color = BG
        patient = T("Patient", 30, BLUE, BOLD).move_to(LEFT * 4.5)
        pbox = SurroundingRectangle(patient, color=BLUE, buff=0.3, stroke_width=2, stroke_opacity=0.5)
        symptoms = VGroup(T("fatigue", 26, WHITE), T("pallor", 26, WHITE),
                          T("dyspnea on exertion", 26, WHITE), T("dizziness", 26, WHITE),
                          T("tachycardia", 26, WHITE),
                          ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).next_to(patient, RIGHT, buff=2.2)
        symptoms.set_opacity(0.85)
        self.play(FadeIn(patient), Create(pbox), run_time=1.0)
        self.play(FadeIn(symptoms, lag_ratio=0.25), run_time=2.0)
        self.wait(2.0)
        self.play(FadeOut(symptoms), FadeOut(pbox), FadeOut(patient), run_time=0.8)

        line1 = T("Treat the cause,", 40, GREEN, BOLD).move_to(UP * 0.9)
        line2 = T("not just the number", 40, GREEN, BOLD).next_to(line1, DOWN, buff=0.4)
        self.add_subcaption("Treat the cause, not just the number.", duration=3)
        self.play(Write(line1), run_time=1.5)
        self.play(Write(line2), run_time=1.5)
        self.wait(3.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
