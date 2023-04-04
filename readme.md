# Matploltlib animations made easy!

This repository is a small utility to easy the use of [matplotlib.animation](https://matplotlib.org/stable/api/animation_api.html).

## Installation
```
pip install git+https://github.com/n-gao/mpl_animation.git
```


## Usage
```python
fig, ax = plt.subplots(figsize=(6, 4))
np.random.seed(2)

x = np.linspace(0, 2*np.pi, 1024)
line, = plt.plot(x, np.sin(x))

x = np.random.normal(size=32) * 2 + np.pi
y = np.random.normal(size=32) / 2
stars, = plt.plot(x, y, '*')

anim = AnimatedFigure(
    fig,
    [
        LineAnimation(
            line, # line chart
            0, # start time
            1, # duration
            Direction.LEFT_TO_RIGHT # direction
        ),
        AnimatedAttribute(
            line, # matplotlib object
            'lw', # attribute
            0, # start value
            4, # end value
            0, # start time
            0.5 # duration
        ),
        AnimatedAttribute(line, 'lw', 4, 0, 0.5, 0.5),
        AnimatedAttribute(stars, 'markersize', 0, 32, 0, 0.3),
        AnimatedAttribute(stars, 'markersize', 32, 0, 0.3, 0.3),
        AnimatedAttribute(stars, 'markersize', 0, 32, 0.6, 0.3),
    ],
    1, # video duration in seconds
    60 # fps
)
# Saving the video
anim.save('example.mp4')
plt.show()
```

### Result
![Example video](video/example.mp4)
