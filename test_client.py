from client import call_llm

# simple fake chunk for testing
test_chunks = ["VIT Bhopal is a private university located in Bhopal, India. It was established in 2017 and offers various undergraduate and postgraduate programs in engineering, management, and other fields. The campus is equipped with modern facilities and promotes research and innovation among its students."]

response = call_llm(test_chunks, "What is VIT Bhopal?")

print("MODEL RESPONSE:\n", response)
