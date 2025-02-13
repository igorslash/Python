from pixellib.instance import instance_segmentation

def object_detection_on_an_image():
    segment_image = instance_segmentation()
    segment_image.load_model("mask_rcnn_coco.h5")
    
    # Выбор целевых классов
    target_classes = segment_image.select_target_classes(person=True, car=True)
    
    # Обработка изображения
    result = segment_image.segmentImage(
        image_path=r"C:\Users\User\PycharmProjects\Training\LlmObject\фото\i.webp",
        show_bboxes=True,
        segment_target_classes=target_classes,
        output_image_name="foto.jpg",
        extract_segmented_objects=True,
        save_extracted_objects=True
    )
    
    # Получение количества объектов
    detected_objects = len(result[0]["class_ids"])
    print(f"Обнаружено объектов: {detected_objects}")

def main():
    object_detection_on_an_image()

if __name__ == "__main__":
    main()
