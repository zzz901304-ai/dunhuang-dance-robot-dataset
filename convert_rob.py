# -*- coding: utf-8 -*-
"""
Convert Hiwonder Tonybot action files (.rob, ACT-40 format) to CSV.
Parsed format (verified against 94 files):
  header : "ACT-40" + version byte + ... ; byte[6] ~= frame count
  frame  : 248 bytes, starting at byte 20, pitch 248
           [0..99]   : 4 zero bytes + 16 x (pos u16 LE + 4 zero bytes)
           [100..243]: 0x5555 padding
           [244..245]: frame execution time in ms (u16 LE)   <-- per-frame time
           [246..247]: 0x5555
"""
import os, csv, struct

SRC_DIR = r'C:\Users\hhhty\Desktop\敦煌舞\敦煌舞--机器人'
OUT_DIR = r'C:\Users\hhhty\Desktop\敦煌舞\dataset'
os.makedirs(OUT_DIR, exist_ok=True)

META = {
    '12345.rob':            ('center_main',  'take_old',     'center main dancer (earlier version)'),
    '29.rob':               ('left_dancer',  'take_29',      'left dancer'),
    '30.rob':               ('left_dancer',  'take_30',      'left dancer (final)'),
    '主c的动作.rob':          ('center_main',  'take_final',   'center main dancer (final)'),
    '右目前11.rob':           ('right_dancer', 'take_11',      'right dancer'),
    '有目前12.rob':           ('right_dancer', 'take_12',      'right dancer'),
    '右目前13.rob':           ('right_dancer', 'take_13',      'right dancer'),
    '右目前14.rob':           ('right_dancer', 'take_14',      'right dancer'),
    '右目前15.rob':           ('right_dancer', 'take_15',      'right dancer (final)'),
    '左目前1.rob':            ('left_dancer',  'take_left1',   'left dancer'),
    '左边的目前.rob':          ('left_dancer',  'take_leftside','left dancer'),
    '后仰.rob':              ('basic',        'back_lean',    'basic: backward lean'),
    '71号向前走俩步.rob':      ('basic',        'walk_2steps',  'basic: walk forward two steps'),
}

def parse_rob(path):
    data = open(path, 'rb').read()
    assert data[:6] == b'ACT-40', 'not an ACT-40 file'
    n = (len(data) - 20) // 248
    frames = []
    for k in range(n):
        s = 20 + k * 248
        if s + 100 > len(data):
            break
        pos = [struct.unpack_from('<H', data, s + 4 + c * 6)[0] for c in range(16)]
        off_t = s + 244
        t = struct.unpack_from('<H', data, off_t)[0] if off_t + 2 <= len(data) else 0
        frames.append((t, pos))
    return frames

def main():
    manifest = []
    for fn, (role, take, desc) in META.items():
        p = os.path.join(SRC_DIR, fn)
        if not os.path.exists(p):
            print('SKIP missing:', fn); continue
        frames = parse_rob(p)
        total_ms = sum(t for t, _ in frames)
        base = f'{role}_{take}'
        csv_path = os.path.join(OUT_DIR, base + '.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['timestamp_ms'] + [f'ch{c+1:02d}' for c in range(16)])
            ts = 0
            for t, pos in frames:
                w.writerow([ts] + pos)
                ts += t
        manifest.append({
            'file': fn, 'csv': base + '.csv', 'role': role, 'take': take,
            'desc': desc, 'frames': len(frames), 'duration_ms': total_ms,
        })
        print(f'{fn:>20} -> {base+".csv":<26} frames={len(frames):4d} dur={total_ms/1000:7.2f}s')
    with open(os.path.join(OUT_DIR, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader(); w.writerows(manifest)
    with open(os.path.join(OUT_DIR, 'README.md'), 'w', encoding='utf-8') as f:
        f.write('# Dunhuang Dance Robot Motion Dataset (Hiwonder Tonybot)\n\n')
        f.write('- Robot: Hiwonder Tonybot, 16 bus-servo channels (IDs 1-16), raw positions 0-1000.\n')
        f.write('- Source: action files (.rob, ACT-40 format) recorded during choreography development.\n')
        f.write('- Each CSV: `timestamp_ms` (cumulative; per-frame time is user-defined in the action editor) + 16 channel values.\n')
        f.write('- Final 3-robot performance: right_dancer_take_15, left_dancer_take_30, center_main_take_final.\n')
        f.write('- All 11 dance sequences + 2 basic actions are released as choreography-evolution records.\n')
    print('\nManifest + README written to', OUT_DIR)

if __name__ == '__main__':
    main()
