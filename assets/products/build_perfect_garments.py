import os
import re
import sys
from PIL import Image, ImageOps, ImageFilter
from garment_masks import (
    mask_polo_premium,
    mask_tshirt_180,
    mask_tshirt_155,
    mask_tshirt_vneck,
    mask_full_polo_woman,
    mask_full_polo_man,
    mask_full_tshirt_woman,
    mask_full_tshirt_man,
    mask_full_tshirt_long,
    mask_full_tank_top,
    mask_full_underwear_tank,
    mask_full_kids_girl,
    mask_full_kids_boy,
    tint_universal
)

# Paths
base_dir = r'c:\Users\USUARIO\Desktop\ACRILAN DOTACIONES'
html_path = os.path.join(base_dir, 'index.html')
raw_dir = os.path.join(base_dir, 'assets', 'products', 'extracted')
prod_main_dir = os.path.join(base_dir, 'assets', 'products')
variants_dir = os.path.join(base_dir, 'assets', 'products', 'variants')
os.makedirs(variants_dir, exist_ok=True)

# Parse products and swatches from index.html
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

prod_blocks = re.findall(r"id:\s*'([^']+)',.*?colors:\s*\[(.*?)\]", html, re.DOTALL)
products_data = {}
for pid, cblock in prod_blocks:
    color_matches = re.findall(r"name:\s*'([^']+)',\s*hex:\s*'([^']+)'", cblock)
    products_data[pid] = [{'name': name, 'hex': hex_val} for name, hex_val in color_matches]

print(f"Loaded {len(products_data)} products and swatches from index.html.")

def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Model specifications mapped to masks and fabric properties
CATALOG_SPECS = {
    'polo-premium': [
        {
            'file': 'sample_p12_xref74.png',
            'mask_fn': mask_polo_premium,
            'is_dark': False, 'is_light': False, 'ref_lum': 128
        }
    ],
    'tshirt-180': [
        {
            'file': 'sample_p13_xref80.png',
            'mask_fn': mask_tshirt_180,
            'is_dark': False, 'is_light': False, 'ref_lum': 128
        }
    ],
    'tshirt-155': [
        {
            'file': 'sample_p14_xref88.png',
            'mask_fn': mask_tshirt_155,
            'is_dark': True, 'is_light': False, 'ref_lum': 128
        }
    ],
    'tshirt-vneck': [
        {
            'file': 'sample_p15_xref98.png',
            'mask_fn': mask_tshirt_vneck,
            'is_dark': True, 'is_light': False, 'ref_lum': 128
        }
    ],
    'full-polo-couple': [
        {
            'file': 'sample_p16_xref109.png',
            'mask_fn': mask_full_polo_woman,
            'is_dark': True, 'is_light': False, 'ref_lum': 128
        },
        {
            'file': 'sample_p16_xref107.png',
            'mask_fn': mask_full_polo_man,
            'is_dark': False, 'is_light': True, 'ref_lum': 185
        }
    ],
    'full-tshirt-couple': [
        {
            'file': 'sample_p17_xref126.png',
            'mask_fn': mask_full_tshirt_woman,
            'is_dark': False, 'is_light': True, 'ref_lum': 150
        },
        {
            'file': 'sample_p17_xref128.png',
            'mask_fn': mask_full_tshirt_man,
            'is_dark': False, 'is_light': False, 'ref_lum': 128
        }
    ],
    'full-tshirt-long': [
        {
            'file': 'sample_p18_xref135.png',
            'mask_fn': mask_full_tshirt_long,
            'is_dark': True, 'is_light': False, 'ref_lum': 128
        }
    ],
    'full-tank-top': [
        {
            'file': 'sample_p19_xref142.png',
            'mask_fn': mask_full_tank_top,
            'is_dark': False, 'is_light': True, 'ref_lum': 185
        }
    ],
    'full-underwear-tank': [
        {
            'file': 'sample_p20_xref147.png',
            'mask_fn': mask_full_underwear_tank,
            'is_dark': False, 'is_light': True, 'ref_lum': 145
        }
    ],
    'full-kids-tshirt': [
        {
            'file': 'sample_p21_xref155.png',
            'mask_fn': mask_full_kids_girl,
            'is_dark': False, 'is_light': False, 'ref_lum': 128
        },
        {
            'file': 'sample_p21_xref157.png',
            'mask_fn': mask_full_kids_boy,
            'is_dark': True, 'is_light': False, 'ref_lum': 128
        }
    ]
}

CANVAS_W = 600
CANVAS_H = 540

total_generated = 0
ONLY = sys.argv[1:]

for pid, specs in CATALOG_SPECS.items():
    if ONLY and pid not in ONLY:
        continue
    print(f"\nProcessing product '{pid}'...")
    
    # 1. Prepare each model component: cropped image + mask + grayscale
    prepared_models = []
    for spec in specs:
        raw_p = os.path.join(raw_dir, spec['file'])
        raw_im = Image.open(raw_p).convert('RGBA')
        bbox = raw_im.getbbox()
        cropped = raw_im.crop(bbox)
        cw, ch = cropped.size
        
        mask = spec['mask_fn'](cropped, spec)
        gray_im = ImageOps.grayscale(cropped.convert('RGB'))
        
        prepared_models.append({
            'cropped': cropped,
            'mask': mask,
            'gray': gray_im,
            'size': (cw, ch),
            'is_dark': spec['is_dark'],
            'is_light': spec['is_light'],
            'ref_lum': spec['ref_lum']
        })
        
    colors = products_data.get(pid, [])
    
    # Outputs:
    # 1. Base display image: assets/products/{pid}.jpg
    # 2. Variants: assets/products/variants/{pid}_c{idx}.jpg
    outputs = [
        (os.path.join(prod_main_dir, f"{pid}.jpg"), None)
    ]
    for idx, c in enumerate(colors):
        outputs.append((os.path.join(variants_dir, f"{pid}_c{idx}.jpg"), hex_to_rgb(c['hex'])))
        
    for out_path, tint_rgb in outputs:
        canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), (248, 250, 252))
        
        if len(prepared_models) == 1:
            m = prepared_models[0]
            rendered = tint_universal(
                m['cropped'], m['mask'], m['gray'], tint_rgb,
                is_dark_fabric=m['is_dark'],
                is_light_fabric=m['is_light'],
                ref_lum=m['ref_lum']
            )
            cw, ch = m['size']
            
            # Scale to 96% height of canvas
            target_h = int(CANVAS_H * 0.96)
            scale = target_h / ch
            target_w = int(cw * scale)
            if target_w > (CANVAS_W * 0.92):
                scale = (CANVAS_W * 0.92) / cw
                target_w = int(cw * scale)
                target_h = int(ch * scale)
                
            resized = rendered.resize((target_w, target_h), Image.Resampling.LANCZOS)
            offset_x = (CANVAS_W - target_w) // 2
            offset_y = (CANVAS_H - target_h) // 2
            canvas.paste(resized, (offset_x, offset_y), resized)
            
        elif len(prepared_models) == 2:
            rendered_pair = []
            for m in prepared_models:
                ren = tint_universal(
                    m['cropped'], m['mask'], m['gray'], tint_rgb,
                    is_dark_fabric=m['is_dark'],
                    is_light_fabric=m['is_light'],
                    ref_lum=m['ref_lum']
                )
                rendered_pair.append(ren)
                
            im1, im2 = rendered_pair
            max_h = int(CANVAS_H * 0.95)
            s1 = max_h / im1.height
            w1 = int(im1.width * s1)
            
            s2 = max_h / im2.height
            w2 = int(im2.width * s2)
            
            gap = 14
            total_w = w1 + w2 + gap
            if total_w > (CANVAS_W * 0.96):
                ratio = (CANVAS_W * 0.96) / total_w
                w1 = int(w1 * ratio)
                w2 = int(w2 * ratio)
                max_h = int(max_h * ratio)
                gap = int(gap * ratio)
                total_w = w1 + w2 + gap
                
            r1 = im1.resize((w1, max_h), Image.Resampling.LANCZOS)
            r2 = im2.resize((w2, max_h), Image.Resampling.LANCZOS)
            
            start_x = (CANVAS_W - total_w) // 2
            start_y = (CANVAS_H - max_h) // 2
            
            canvas.paste(r1, (start_x, start_y), r1)
            canvas.paste(r2, (start_x + w1 + gap, start_y), r2)
            
        canvas.save(out_path, quality=92)
        total_generated += 1

print(f"\nDone! Successfully regenerated {total_generated} images (10 base + {total_generated - 10} color variants).")
