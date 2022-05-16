# This code Snippet is directly copied from
# https://realpython.com/pysimplegui-python/#integrating-opencv-with-pysimplegui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
