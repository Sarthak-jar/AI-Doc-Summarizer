from transformers import pipeline
import math

# Initialize the summarizer pipeline
# Using a specific model version ensures consistency
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    """
    Summarizes a long text by breaking it into chunks and summarizing each chunk.
    """
    # Basic cleanup
    text = text.replace('\n', ' ').replace('\r', '').strip()
    
    # The model's max token length is 1024. We'll use a slightly smaller chunk size
    # to be safe and allow for model-specific tokens.
    max_chunk_size = 800  # A safe chunk size in tokens
    
    # A simple way to estimate token count is by word count (it's not perfect but good enough)
    words = text.split()
    
    # If the text is already short, summarize it directly
    if len(words) < max_chunk_size:
        try:
            summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"An error occurred during summarization: {e}"

    # Chunking logic for long texts
    chunks = []
    current_chunk_words = []
    for word in words:
        current_chunk_words.append(word)
        # When a chunk reaches the desired size, add it to the list
        if len(current_chunk_words) == max_chunk_size:
            chunks.append(" ".join(current_chunk_words))
            # Overlap chunks to maintain context
            current_chunk_words = current_chunk_words[-50:] # Overlap by 50 words
    
    # Add the last remaining chunk
    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))

    # Summarize each chunk
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        # We can dynamically adjust the length of the summary based on chunk size
        # A simple heuristic: 15% of the chunk length, with a min and max
        num_words = len(chunk.split())
        summary_max_len = max(40, min(150, int(num_words * 0.2)))
        summary_min_len = max(20, int(num_words * 0.1))

        try:
            summary = summarizer(chunk, max_length=summary_max_len, min_length=summary_min_len, do_sample=False)
            chunk_summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk {i+1}: {e}")
            # Optional: append the chunk itself or an error message if summarization fails
            # chunk_summaries.append("[Could not summarize this section]")

    # Combine the summaries
    full_summary = "\n- ".join(chunk_summaries)
    
    # (Optional but recommended) Final recursive summary for coherence
    # If the combined summary is too long, we can summarize it again!
    if len(full_summary.split()) > 400:
        final_summary = summarizer(full_summary, max_length=250, min_length=50, do_sample=False)
        return final_summary[0]['summary_text']
        
    return "- " + full_summary