import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk, os
from tqdm import tqdm

nltk.download("punkt")

# Read file content
with open("input.txt", "r") as file:
    file_content = file.read().strip()

# Load the model and tokenizer
checkpoint = "pszemraj/led-large-book-summary"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print(device)

# Tokenize sentences
sentences = nltk.tokenize.sent_tokenize(file_content)

# Calculate input file statistics
num_sentences = len(sentences)
num_words = sum(len(sentence.split()) for sentence in sentences)
num_chars = sum(len(sentence) for sentence in sentences)

print("this model's max size is: ")
print(tokenizer.model_max_length)
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

print("chunking completed")
num_chunks = len(chunks)

# Create the output directory if it doesn't exist
output_dir = "/root/.cache/output"
os.makedirs(output_dir, exist_ok=True)

# Set the output file name
output_file_path = os.path.join(output_dir, "summary.txt")

# Process each chunk and generate summaries
with open(output_file_path, "w") as output_file:
    for i, chunk in tqdm(enumerate(chunks), total=num_chunks, desc="Generating summaries"):
        inputs = tokenizer(chunk, return_tensors="pt")
        inputs = inputs.to(device)  # Move inputs to GPU if available
        outputs = model.generate(**inputs)
        summary = tokenizer.decode(outputs[0])

        # print summary
        print(summary)
        
        # Write the summary to the output file
        output_file.write(summary + "\n")


        # Print progress information
        tqdm.write(f"Processed {i+1}/{num_chunks} chunks")

# Calculate output file statistics
with open(output_file_path, "r") as output_file:
    output_content = output_file.read().strip()

num_summary_sentences = len(nltk.tokenize.sent_tokenize(output_content))
num_summary_words = sum(len(sentence.split()) for sentence in nltk.tokenize.sent_tokenize(output_content))
num_summary_chars = len(output_content)

# Print input and output file statistics

print(f"Number of characters in summary: {num_summary_chars}")
print(f"Number of words in summary: {num_summary_words}")
print(f"Number of sentences in summary: {num_summary_sentences}")

print(f"Number of characters in input file: {num_chars}")
print(f"Number of words in input file: {num_words}")
print(f"Number of sentences in input file: {num_sentences}")
print(f"Number of chunks: {num_chunks}")

tqdm.write(f"Finished processing {num_chunks} chunks in {tqdm.format_interval(tqdm.tqdm.get_loop_times()[0])}")
