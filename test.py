from ultralytics import YOLO

model = YOLO("ai_models/best.pt")

print(model.names)

results = model("test.jpg", save=True)

print("Detection completed")