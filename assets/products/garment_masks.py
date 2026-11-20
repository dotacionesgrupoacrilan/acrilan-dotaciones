import os
import colorsys
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageChops

def connected_from_seed(mask, seed, close=5):
    w, h = mask.size
    core = mask.point(lambda v: 255 if v >= 180 else 0)
    core = core.filter(ImageFilter.MaxFilter(close)).filter(ImageFilter.MinFilter(close))
    ImageDraw.floodfill(core, seed, 128, thresh=0)
    comp = core.point(lambda v: 255 if v == 128 else 0)
    inv = Image.new('L', (w + 2, h + 2), 0)
    inv.paste(comp, (1, 1))
    ImageDraw.floodfill(inv, (0, 0), 100, thresh=0)
    comp = inv.crop((1, 1, w + 1, h + 1)).point(lambda v: 0 if v == 100 else 255)
    return comp

def absorb_fringe(mask, im, radius=2):
    alpha = im.split()[3]
    near_bg = alpha.point(lambda v: 255 if v < 128 else 0).filter(ImageFilter.MaxFilter(radius * 2 + 1))
    hard = mask.point(lambda v: 255 if v >= 128 else 0)
    grown = hard.filter(ImageFilter.MaxFilter(radius * 2 + 1))
    add = ImageChops.multiply(grown, near_bg)
    return ImageChops.lighter(mask, add)

def grow_edges(mask, im, condition_fn, steps=2):
    w, h = mask.size
    p = im.load()
    m = mask.copy()
    for _ in range(steps):
        grown = m.filter(ImageFilter.MaxFilter(3))
        gp, mp = grown.load(), m.load()
        for y in range(h):
            for x in range(w):
                if mp[x, y] >= 200 or gp[x, y] < 200: continue
                r, g, b, a = p[x, y]
                if a < 30: continue
                if condition_fn(x, y, r, g, b):
                    mp[x, y] = 230
    return m

# ---- MASKS PER MODEL ----

def mask_polo_premium(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            gr = g - max(r, b)
            if gr <= 2: continue
            mp[x, y] = int(min(255, (gr - 2) * 255 / 8) * a / 255)
    m = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    m = grow_edges(m, im, lambda x, y, r, g, b: not (r > g + 12 and r > b + 15) and not (b > g + 6), steps=1)
    return m.filter(ImageFilter.GaussianBlur(0.8))

def mask_tshirt_180(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if vv < 0.12: continue
            hd = (hh * 360 + 180) % 360 - 180
            ad = abs(hd) if hd > -20 else 99
            if ad >= 9.0 or ss <= 0.48: continue
            kh = 1.0 if ad <= 5.0 else (9.0 - ad) / 4.0
            ks = min(1.0, (ss - 0.48) / 0.14)
            gr = max(g, b) / max(r, 1)
            shift = 0.14 * min(1.0, max(0.0, (vv - 0.80) / 0.10))
            lo, hi = 0.27 + shift, 0.34 + shift
            kr = 1.0 if gr <= lo else max(0.0, (hi - gr) / (hi - lo))
            mp[x, y] = int(255 * kh * ks * kr * a / 255)
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_tshirt_155(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 505 or y < 145: continue
            if (y > 304 and x < 50) or (y > 318 and x > 230): continue
            skin = (r > 60 and r > g + 10 and r > b + 15) or (r > 100 and r > b + 10)
            if skin: continue
            jeans = y > 498 and ((b > r + 8 and b > 30) or (r > 35 and g > 35 and b > 45))
            if jeans: continue
            if max(r, g, b) < 42:
                mp[x, y] = 255
            elif max(r, g, b) < 95 and not skin:
                mp[x, y] = 220
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    m = grow_edges(m, im, lambda x, y, r, g, b: y <= 504 and not ((r > 80 and r > g + 10 and r > b + 15) or (r > 110 and r > b + 10)) and not (y > 498 and (b > r + 8 or b > 35)) and (y <= 318 or (50 <= x <= 230)), steps=1)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_tshirt_vneck(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 504 or y < 145: continue
            if (y > 300 and x < 40) or (y > 305 and x > 248): continue
            skin = (r > 60 and r > g + 10 and r > b + 15) or (r > 100 and r > b + 10)
            if skin: continue
            jeans = y > 498 and (r > 40 and g > 40 and b > 55)
            if jeans: continue
            if max(r, g) < 40 and b < 55:
                mp[x, y] = 255
            elif max(r, g) < 75 and b < 85 and not skin:
                mp[x, y] = 220
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    m = grow_edges(m, im, lambda x, y, r, g, b: y <= 504 and not ((r > 80 and r > g + 10 and r > b + 15) or (r > 110 and r > b + 10)) and not (y > 498 and (b > 50 and r > 35)), steps=1)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_polo_woman(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 430 or y < 145: continue
            skin = (r > 80 and r > g + 15 and r > b + 20) or (r > 120 and r > b + 15)
            if skin: continue
            jeans = y > 426 and (b > g + 15 or b > 45)
            if jeans: continue
            if max(r, g) < 55 and b < 70:
                mp[x, y] = 255
            elif max(r, g) < 85 and b < 100 and not skin:
                mp[x, y] = 200
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_polo_man(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 465 or y < 112: continue
            skin = (r > g + 12 and r > b + 22) or (r > 130 and r > b + 18)
            if skin: continue
            jeans = y > 462 and (r < 100 and g < 110 and b < 130)
            if jeans: continue
            if (r + g + b) / 3 > 140 and abs(r - g) < 18 and abs(r - b) < 22:
                mp[x, y] = 255
            elif (r + g + b) / 3 > 80 and abs(r - g) < 18 and abs(r - b) < 22 and not skin:
                mp[x, y] = 220
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_tshirt_woman(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 494 or y < 110: continue
            skin = (r > g + 15 and r > b + 25) or (r > 135 and r > b + 18)
            if skin: continue
            if abs(r - g) < 16 and abs(r - b) < 20 and 70 < (r + g + b) / 3 < 235:
                mp[x, y] = 255
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_tshirt_man(im, spec=None):
    return mask_tshirt_180(im, spec)

def mask_full_tshirt_long(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 312 or y < 98: continue
            if x < 75 and (r + g + b) / 3 > 60: continue
            skin = (r > 80 and r > g + 15 and r > b + 20) or (r > 110 and r > b + 15)
            if skin: continue
            if max(r, g, b) < 40:
                mp[x, y] = 255
            elif max(r, g, b) < 75 and not skin and not (x < 75):
                mp[x, y] = 200
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_tank_top(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 482 or y < 122: continue
            skin = (r > g + 12 and r > b + 20) or (r > 125 and r > b + 15)
            if skin: continue
            pants = y > 476 and (r < 60 and g < 60 and b < 80)
            if pants: continue
            if (r + g + b) / 3 > 140 and abs(r - g) < 18 and abs(r - b) < 20:
                mp[x, y] = 255
            elif (r + g + b) / 3 > 80 and abs(r - g) < 18 and abs(r - b) < 20 and not skin:
                mp[x, y] = 200
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_underwear_tank(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y > 464 or y < 208: continue
            skin = (r > g + 15 and r > b + 25) or (r > 120 and r > b + 20)
            if skin: continue
            pants = y > 460 and (b > 50 and b > r + 20)
            if pants: continue
            if abs(r - g) < 18 and abs(r - b) < 22 and 70 < (r + g + b) / 3 < 210:
                mp[x, y] = 255
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_kids_girl(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if vv < 0.12: continue
            hd = (hh * 360 + 180) % 360 - 180
            ad = abs(hd) if hd > -20 else 99
            if ad >= 9.0 or ss <= 0.78: continue
            kh = 1.0 if ad <= 5.0 else (9.0 - ad) / 4.0
            ks = min(1.0, (ss - 0.78) / 0.12)
            gr = max(g, b) / max(r, 1)
            kr = 1.0 if gr <= 0.12 else max(0.0, (0.20 - gr) / 0.08)
            mp[x, y] = int(255 * kh * ks * kr * a / 255)
    m = connected_from_seed(m, (w // 2, int(h * 0.5)))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

def mask_full_kids_boy(im, spec=None):
    w, h = im.size
    p = im.load()
    m = Image.new('L', (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a < 30: continue
            if y < 132 or y > 375: continue
            if (r > 75 and r > g + 10 and r > b + 15) or (r > 115 and r > b + 18):
                continue
            if 232 <= y <= 278 and (r > 55 and r > b):
                continue
            if y > 370 and ((b > 60 and r > 30) or (r > 40 and g > 50 and b > 75)):
                continue
            if (b > r + 3) and max(r, g) < 55:
                mp[x, y] = 255
            elif max(r, g) < 35 and b < 65:
                mp[x, y] = 255
            elif max(r, g) < 70 and b < 85 and b >= r:
                mp[x, y] = 220
    m = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    m = absorb_fringe(m, im, radius=2)
    return m.filter(ImageFilter.GaussianBlur(0.7))

# ---- UNIVERSAL TINTING ENGINE ----

def tint_universal(im, mask, gray, target_rgb, is_dark_fabric=False, is_light_fabric=False, ref_lum=128):
    if target_rgb is None:
        return im
    tr, tg, tb = target_rgb
    target_lum = 0.299 * tr + 0.587 * tg + 0.114 * tb
    out = im.copy()
    op = out.load()
    gp = gray.load()
    mp = mask.load()
    ip = im.load()
    w, h = im.size
    
    for y in range(h):
        for x in range(w):
            mv = mp[x, y] / 255.0
            if mv < 0.02: continue
            r, g, b, a = ip[x, y]
            lum = gp[x, y]
            
            if is_dark_fabric:
                norm_lum = max(0.0, min(1.0, (lum - 4.0) / 14.0))
                if target_lum > 220:
                    s = 0.82 + norm_lum * 0.18
                    nr, ng, nb = int(tr * s), int(tg * s), int(tb * s)
                elif target_lum < 35:
                    s = 0.70 + norm_lum * 0.50
                    nr, ng, nb = int(tr * s), int(tg * s), int(tb * s)
                else:
                    s = 0.68 + norm_lum * 0.55
                    nr, ng, nb = min(255, int(tr * s)), min(255, int(tg * s)), min(255, int(tb * s))
            elif is_light_fabric:
                s = lum / max(1.0, ref_lum)
                if target_lum < 35:
                    nr = min(255, int(s * 25))
                    ng = min(255, int(s * 25))
                    nb = min(255, int(s * 30))
                elif target_lum > 220:
                    k = min(1.0, max(0.0, (lum - 150) / 95.0))
                    s = 0.82 + k * 0.18
                    nr, ng, nb = int(tr * s), int(tg * s), int(tb * s)
                else:
                    if s <= 1.0:
                        nr, ng, nb = int(tr * s), int(tg * s), int(tb * s)
                    else:
                        k = min(1.0, (s - 1.0) * 0.6)
                        nr = min(255, int(tr + (255 - tr) * k))
                        ng = min(255, int(tg + (255 - tg) * k))
                        nb = min(255, int(tb + (255 - tb) * k))
            else:
                s = lum / max(1.0, ref_lum)
                if s <= 1.0:
                    nr, ng, nb = int(tr * s), int(tg * s), int(tb * s)
                else:
                    k = min(1.0, (s - 1.0) * 0.6)
                    nr = min(255, int(tr + (255 - tr) * k))
                    ng = min(255, int(tg + (255 - tg) * k))
                    nb = min(255, int(tb + (255 - tb) * k))
                    
            final_r = int(r * (1 - mv) + nr * mv)
            final_g = int(g * (1 - mv) + ng * mv)
            final_b = int(b * (1 - mv) + nb * mv)
            op[x, y] = (final_r, final_g, final_b, a)
            
    return out
