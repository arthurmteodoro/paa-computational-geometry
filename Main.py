import tkinter as tk
from Representations.Circle import Circle
from Representations.Line import Line
from Representations.LineSegment import LineSegment
from Representations.Point import Point
from Representations.Polygon import Polygon
import Problems.ClassicalProblems as classics
from Problems.Complex_Problems.Voronoi import Voronoi
from Problems.Complex_Problems.Closest_Pair_Points import ClosestPair
from Problems.Complex_Problems.Convex_Hull import ConvexHull
import copy


class MainWindow:
    RADIUS = 2
    LOCK = True

    def __init__(self, master):
        self.master = master
        self.master.title("Trabalho PAA")

        self.master.bind('<Return>', self.onPressReturn)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.classicsMenu = tk.Menu(self.menu)
        self.complexMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Problemas Clássicos", menu=self.classicsMenu)
        self.menu.add_cascade(label="Problemas Complexos", menu=self.complexMenu)
        self.classicsMenu.add_command(label="Calcular...", command=self.calcular)
        self.classicsMenu.add_command(label="Dobrar em Triangulos", command=self.calcular_tringulacao)

        self.complexMenu.add_command(label="Fecho Convexo", command=self.calcular_fecho_convexo)
        self.complexMenu.add_command(label="Par mais próximo", command=self.calcular_ponto_mais_proximo)
        self.complexMenu.add_command(label="Voronoi", command=self.calcular_voronoi)

        self.frmMain = tk.Frame(self.master)
        self.frmMain.pack(side=tk.LEFT)

        self.w = tk.Canvas(self.frmMain, width=500, height=500)
        self.w.config(background='white')
        self.w.bind('<Button-1>', self.onClick)
        self.w.pack(side=tk.RIGHT)

        self.frmButtons = tk.Frame(self.master)
        self.frmButtons.pack(side=tk.RIGHT)

        self.btnCirculo = tk.Button(self.frmButtons, text="Criar Círculo", width=15, command=self.onClickCriarCirculo)
        self.btnCirculo.pack(side=tk.TOP)

        self.btnLinha = tk.Button(self.frmButtons, text="Criar Linha", width=15, command=self.onClickCriarLinha)
        self.btnLinha.pack(side=tk.TOP)

        self.btnSegmento = tk.Button(self.frmButtons, text="Criar Segmento", width=15, command=self.onCickCriarSegmento)
        self.btnSegmento.pack(side=tk.TOP)

        self.btnPonto = tk.Button(self.frmButtons, text="Criar Ponto", width=15, command=self.onClickCriarPonto)
        self.btnPonto.pack(side=tk.TOP)

        self.btnPolygon = tk.Button(self.frmButtons, text="Criar Polígono", width=15,
                                    command=self.onClickCriarPoligono)
        self.btnPolygon.pack(side=tk.TOP)

        self.btnClear = tk.Button(self.frmButtons, text='Clear', width=15, command=self.onClickClear)
        self.btnClear.pack(side=tk.BOTTOM, pady=50)

        self.circles = []
        self.lines = []
        self.segments = []
        self.points = []
        self.polygons = []

        self.pts = []

    def onClickClear(self):
        self.LOCK = True
        self.w.delete(tk.ALL)
        self.circles.clear()
        self.lines.clear()
        self.segments.clear()
        self.points.clear()
        self.polygons.clear()
        self.liberaTodosBotoes()
        self.pts.clear()

    def onClick(self, event):
        if not self.LOCK:
            self.w.create_oval(event.x-self.RADIUS, event.y-self.RADIUS, event.x+self.RADIUS,
                               event.y+self.RADIUS, fill="black")
            self.pts.append((event.x, event.y))

            if self.btnCirculo['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    distance = classics.distance_between_two_points(p1, p2)
                    circle = Circle(p1, int(distance))
                    self.circles.append(circle)

                    self.draw_circle(p1.get_x(), p1.get_y(), circle.get_radius())
                    nome = "Circ"+str(len(self.circles))
                    self.w.create_text(p1.get_x(), p1.get_y()+circle.get_radius()+7, text=nome)

                    self.liberaTodosBotoes()
                    self.LOCK = True
                    self.pts.clear()
            elif self.btnLinha['state'] == tk.NORMAL:
                pass
            elif self.btnSegmento['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    seg = LineSegment(p1, p2)
                    self.segments.append(seg)

                    self.w.create_line(p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y(), fill='red')
                    nome = "Seg"+str(len(self.segments))
                    self.w.create_text((p1.get_x()+p2.get_x())/2, (p1.get_y()+p2.get_y())/2, text=nome)

                    self.liberaTodosBotoes()
                    self.LOCK = True
                    self.pts.clear()
            elif self.btnPonto['state'] == tk.NORMAL:
                p = Point(self.pts[0][0], self.pts[0][1])
                self.points.append(p)

                nome = "Ptn"+str(len(self.points))
                self.w.create_text(p.get_x(), p.get_y()+10, text=nome)
                self.pts.clear()
            elif self.btnPolygon['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    seg = LineSegment(p1, p2)
                    self.polygons[len(self.polygons)-1].add_segment(seg)

                    self.w.create_line(p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y(), fill='blue')

                    del self.pts[0]

    def onClickCriarCirculo(self):
        self.LOCK = False
        self.blockButtons(self.btnCirculo)

    def onClickCriarLinha(self):
        self.LOCK = False
        self.blockButtons(self.btnLinha)

    def onCickCriarSegmento(self):
        self.LOCK = False
        self.blockButtons(self.btnSegmento)

    def onClickCriarPonto(self):
        self.LOCK = False
        self.blockButtons(self.btnPonto)

    def onClickCriarPoligono(self):
        self.LOCK = False
        self.blockButtons(self.btnPolygon)
        self.polygons.append(Polygon())

    def calcular(self):
        pass

    def onPressReturn(self, event):
        if not self.LOCK:
            if self.btnPonto['state'] == tk.NORMAL:
                self.LOCK = True
                self.liberaTodosBotoes()
            elif self.btnPolygon['state'] == tk.NORMAL:
                if len(self.polygons[len(self.polygons)-1].get_list_points()) >= 3:
                    p_i = self.polygons[len(self.polygons)-1].get_list_points()[0]
                    p_f = self.polygons[len(self.polygons)-1].get_list_points()[len(self.polygons[len(self.polygons)-1].get_list_points())-1]

                    seg = LineSegment(p_i, p_f)
                    self.polygons[len(self.polygons) - 1].add_segment(seg)

                    self.w.create_line(p_i.get_x(), p_i.get_y(), p_f.get_x(), p_f.get_y(), fill='blue')
                    nome = "Poly"+str(len(self.polygons))
                    self.w.create_text(p_i.get_x(), p_i.get_y()+15, text=nome)

                    self.LOCK = True
                    self.liberaTodosBotoes()
                    self.pts.clear()

    def blockButtons(self, button: tk.Button):
        self.btnCirculo.configure(state=tk.DISABLED)
        self.btnLinha.configure(state=tk.DISABLED)
        self.btnSegmento.configure(state=tk.DISABLED)
        self.btnPonto.configure(state=tk.DISABLED)
        self.btnPolygon.configure(state=tk.DISABLED)
        button.configure(state=tk.NORMAL)

    def liberaTodosBotoes(self):
        self.btnCirculo.configure(state=tk.NORMAL)
        self.btnLinha.configure(state=tk.NORMAL)
        self.btnSegmento.configure(state=tk.NORMAL)
        self.btnPonto.configure(state=tk.NORMAL)
        self.btnPolygon.configure(state=tk.NORMAL)

    def draw_circle(self, x, y, r, **kwargs):
        self.w.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def calcular_fecho_convexo(self):
        convex = ConvexHull(self.points)
        hull = convex.calcule()

        n = len(hull)
        for i in range(len(hull)):
            self.w.create_line(hull[i].get_x(), hull[i].get_y(), hull[(i+1) % n].get_x(),
                               hull[(i+1) % n].get_y(), fill='blue')

    def calcular_ponto_mais_proximo(self):
        closest_point = ClosestPair(self.points)

        res = closest_point.get_closest_points()
        self.w.create_line(res[1].get_x(), res[1].get_y(), res[2].get_x(), res[2].get_y(), fill='green')

    def calcular_voronoi(self):
        voronoi = Voronoi(self.points)
        voronoi.process()
        lines = voronoi.get_output()

        for i in lines:
            p0 = i.get_a()
            p1 = i.get_b()
            self.w.create_line(p0.get_x(), p0.get_y(), p1.get_x(), p1.get_y(), fill='blue')

    def calcular_tringulacao(self):
        pts = copy.deepcopy(self.polygons[0].get_list_points())
        plist = pts[::-1] if classics.is_clockwise(self.polygons[0]) else pts[:]
        tri = []
        while len(plist) >= 3:
            ear = classics.get_ear(plist)
            if ear == []:
                break
            tri.append(ear)

        for p0, p1, p2 in tri:
            self.w.create_line(p0.get_x(), p0.get_y(), p1.get_x(), p1.get_y())
            self.w.create_line(p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y())
            self.w.create_line(p2.get_x(), p2.get_y(), p0.get_x(), p0.get_y())



if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()