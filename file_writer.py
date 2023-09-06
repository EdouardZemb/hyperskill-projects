def write_to_output(content, output_file):
    try:
        with open(output_file, "w") as output:
            output.write(content)
    except Exception as e:
        print(f"An unexpected error occurred while writing to '{output_file}': {e}")
        sys.exit(1)
