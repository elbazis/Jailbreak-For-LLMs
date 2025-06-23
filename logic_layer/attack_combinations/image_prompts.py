from PIL import Image, ImageDraw, ImageFont
import os
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from logic_layer.consts import BASE_PATH

def wrap_text_to_pixels(text, draw, font, max_width):
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def _convert_prompt_to_image(image_path, name, prompt, width=1200, margin=40, font_size=36):
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)  # For macOS
    except:
        font = ImageFont.load_default()
        print("Arial not found, using default font.")

    dummy_img = Image.new('RGB', (width, 100))
    draw = ImageDraw.Draw(dummy_img)

    wrapped_text = wrap_text_to_pixels(prompt, draw, font, width - 2 * margin)

    ascent, descent = font.getmetrics()
    line_height = ascent + descent + 10
    height = margin * 2 + line_height * len(wrapped_text)

    # Create actual image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw text
    y = margin
    for line in wrapped_text:
        draw.text((margin, y), line, font=font, fill='black')
        y += line_height

    os.makedirs(image_path, exist_ok=True)
    img.save(f"{image_path}/{name}_prompt.png", dpi=(300, 300))

def save_prompts_as_images(prompts_path, image_path):
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(prompts_path)
    for name, prompt in names_and_prompts:
        _convert_prompt_to_image(image_path, name, prompt)

# original english prompts
save_prompts_as_images(f"../../{BASE_PATH}/first_dataset.csv",
                       "../../data_layer/images_prompts/original_prompts_images")

# באסקית
save_prompts_as_images("../../data_layer/translated_jailbreak_prompts/eu_prompts.csv",
                       "../../data_layer/images_prompts/eu_prompts_images")

# וולשית
save_prompts_as_images("../../data_layer/translated_jailbreak_prompts/cy_prompts.csv",
                       "../../data_layer/images_prompts/cy_prompts_images")

# אסטונית
save_prompts_as_images("../../data_layer/translated_jailbreak_prompts/et_prompts.csv",
                       "../../data_layer/images_prompts/et_prompts_images")
