import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk, os

nltk.download("punkt")

# Read file content
with open("input.txt", "r") as file:
    file_content = file.read().strip()

# Load the model and tokenizer
checkpoint = "philschmid/bart-large-cnn-samsum"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print(device)

# Tokenize sentences
sentences = nltk.tokenize.sent_tokenize(file_content)

# Create chunks that fit within the model's maximum sequence length
chunks = []
chunk = ""
for sentence in sentences:
    tokenized_sentence = tokenizer.tokenize(sentence)
    new_length = len(tokenized_sentence) + len(tokenizer.tokenize(chunk)) + tokenizer.num_special_tokens_to_add()

    if new_length <= tokenizer.model_max_length:
        chunk += sentence + " "
    else:
        chunks.append(chunk.strip())
        chunk = sentence + " "
        
    if sentence == sentences[-1]:
        chunks.append(chunk.strip())

# Create the output directory if it doesn't exist
output_dir = "/root/.cache/output"
os.makedirs(output_dir, exist_ok=True)

# Set the output file name
output_file_path = os.path.join(output_dir, "summary.txt")

# Process each chunk and generate summaries
with open(output_file_path, "w") as output_file:
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt")
        inputs = inputs.to(device)  # Move inputs to GPU if available
        outputs = model.generate(**inputs)
        summary = tokenizer.decode(outputs[0])

        # Write the summary to the output file
        output_file.write(summary + "\n")
