from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation


class Animation:
    start: float
    duration: float
    ended: bool = False

    def __init__(self, start: float, duration: float):
        self.start = start
        self.duration = duration

    def update(self, time):
        if time < self.start:
            return
        if time >= self.start + self.duration:
            if self.ended:
                return
            self.ended = True
            return self(1)
        return self((time - self.start)/self.duration)

    def __call__(self, time):
        raise NotImplementedError()


class AnimatedAttribute(Animation):
    obj: object
    attribute: str
    val_init: float
    val_end: float

    def __init__(
            self,
            obj,
            attribute: str,
            val_init: float,
            val_end: float,
            start: float,
            duration: float):
        super().__init__(start, duration)
        self.val_init = val_init
        self.val_end = val_end
        self.attribute = attribute
        self.obj = obj
        if isinstance(self.attribute, str):
            self._setter = getattr(obj, f'set_{self.attribute}')
        elif callable(self.attribute):
            self._setter = self.attribute
        else:
            raise ValueError()

    def init(self):
        self._setter(self.val_init)
        return [self.obj]

    def __call__(self, time):
        self._setter(time * (self.val_end - self.val_init) + self.val_init)


class Direction(Enum):
    LEFT_TO_RIGHT = 'left->right'
    RIGHT_TO_LEFT = 'right->left'
    INV_LEFT_TO_RIGHT = 'left<-right'
    INV_RIGHT_TO_LEFT = 'right<-left'


class LineAnimation(AnimatedAttribute):
    direction: str

    def __init__(
        self,
        line_chart: plt.Line2D,
        start: float,
        duration: float,
        direction: str | Direction = Direction.LEFT_TO_RIGHT
    ):
        x, y = line_chart.get_data()
        N = len(x)
        direction = Direction(direction)

        def update_items(time):
            n = int(time * N)
            if direction is Direction.LEFT_TO_RIGHT:
                idx = slice(None, n)
            elif direction is Direction.RIGHT_TO_LEFT:
                idx = slice(-n, None)
            elif direction is Direction.INV_RIGHT_TO_LEFT:
                idx = slice(n, None)
            elif direction is Direction.INV_LEFT_TO_RIGHT:
                idx = slice(None, -n)
            line_chart.set_data(x[idx], y[idx])
        super().__init__(
            line_chart,
            update_items,
            0,
            1,
            start,
            duration
        )


class AnimatedFigure():
    figure: plt.Figure
    animations: list[Animation]
    duration: float
    func_animation: FuncAnimation

    def __init__(self, figure: plt.Figure, animations: list[Animation], duration: float, fps: float = 30):
        self.animations = animations
        self.figure = figure
        self.duration = duration
        self.fps = fps
        self.func_animation = FuncAnimation(
            self.figure,
            self.update,
            frames=np.linspace(0, duration, int(duration*fps)),
            init_func=self.init,
            blit=False,
            repeat=False
        )

    def init(self):
        result = []
        for ani in self.animations:
            result += ani.init()
        return result

    def update(self, time):
        for ani in self.animations:
            ani.update(time)

    def save(self, name):
        writervideo = FFMpegWriter(fps=self.fps)
        self.func_animation.save(name, writer=writervideo)
