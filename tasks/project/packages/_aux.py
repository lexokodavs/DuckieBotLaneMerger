def set_all_leds(leds, r, g, b):
    leds.set_rgb(0, [r, g, b])
    leds.set_rgb(2, [r, g, b])
    leds.set_rgb(3, [r, g, b])
    leds.set_rgb(4, [r, g, b])