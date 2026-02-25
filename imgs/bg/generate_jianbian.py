import argparse
from PIL import Image

# 颜色字符串转RGB元组
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_gradient(width, height, start_color, mid_color, end_color, direction):
    img = Image.new("RGB", (width, height), start_color)
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if direction == 'vertical':
                ratio = y / (height - 1)
            elif direction == 'horizontal':
                ratio = x / (width - 1)
            elif direction == 'diagonal':
                ratio = (x + y) / (width + height - 2)
            else:
                ratio = y / (height - 1)
            # 三段渐变：前半段 start->mid，后半段 mid->end
            if mid_color is not None:
                if ratio < 0.5:
                    sub_ratio = ratio / 0.5
                    r = int(start_color[0] * (1 - sub_ratio) + mid_color[0] * sub_ratio)
                    g = int(start_color[1] * (1 - sub_ratio) + mid_color[1] * sub_ratio)
                    b = int(start_color[2] * (1 - sub_ratio) + mid_color[2] * sub_ratio)
                else:
                    sub_ratio = (ratio - 0.5) / 0.5
                    r = int(mid_color[0] * (1 - sub_ratio) + end_color[0] * sub_ratio)
                    g = int(mid_color[1] * (1 - sub_ratio) + end_color[1] * sub_ratio)
                    b = int(mid_color[2] * (1 - sub_ratio) + end_color[2] * sub_ratio)
            else:
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pixels[x, y] = (r, g, b)
    return img

def main():
    parser = argparse.ArgumentParser(description='生成渐变背景图片')
    parser.add_argument('--width', type=int, default=1920, help='图片宽度')
    parser.add_argument('--height', type=int, default=1080, help='图片高度')
    parser.add_argument('--start', type=str, default='#e3f0ff', help='起始颜色（16进制）')
    parser.add_argument('--mid', type=str, default=None, help='中间颜色（16进制，可选）')
    parser.add_argument('--end', type=str, default='#a18cd1', help='结束颜色（16进制）')
    parser.add_argument('--direction', type=str, choices=['vertical', 'horizontal', 'diagonal'], default='diagonal', help='渐变方向')
    parser.add_argument('--output', type=str, default='default.jpg', help='输出文件名')
    args = parser.parse_args()

    start_color = hex_to_rgb(args.start)
    end_color = hex_to_rgb(args.end)
    mid_color = hex_to_rgb(args.mid) if args.mid else None
    img = generate_gradient(args.width, args.height, start_color, mid_color, end_color, args.direction)
    print(f"生成渐变背景 {args.output} 完成！ 尺寸: {args.width}x{args.height} 渐变: {args.direction} 颜色: {args.start} -> {args.mid if args.mid else ''} -> {args.end}")
    img.save(args.output, "JPEG")

if __name__ == '__main__':
    main()
