def read_chunks(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return [data[i:i+4] for i in range(0, len(data), 4)]

def find_rich_and_key(chunks, rich_tag):
    for i, chunk in enumerate(chunks):
        if chunk == rich_tag:
            return i, i + 1 # rich idx, key idx
    raise ValueError("Rich tag not found")

def decode_chunks(chunks, rich_idx, key, dans_tag):
    key = int.from_bytes(key, 'little')
    dans = int.from_bytes(dans_tag, 'little')
    result = []

    for d in reversed(chunks[:rich_idx]):
        val = int.from_bytes(d, 'little') ^ key
        result.append(val.to_bytes(4, 'little'))
        if val == dans:
            break

    result.reverse()
    result.extend([chunks[rich_idx], chunks[rich_idx+1]])
    print(result)
    return result

def write_chunks(decoded, savepath):
    with open(savepath, 'wb') as f:
        for chunk in decoded:
            f.write(chunk)

def write_parse_chunks(decoded_chunks, savepath):
    parse_chunks = decoded_chunks[:4] + [decoded_chunks[i] + decoded_chunks[i + 1] for i in range(4, len(decoded_chunks) - 6, 2)] + decoded_chunks[-2:]
    with open(savepath + ".txt", 'w') as f:
        for i, d in enumerate(parse_chunks):
            if len(d) == 4:
                line = f"{i:02d} : 0x{d.hex()} {d}"
            else:
                build_id = int.from_bytes(d[:2], 'little')
                product_id = int.from_bytes(d[2:4], 'little')
                count = int.from_bytes(d[4:8], 'little')
                line = f"{i:02d} : 0x{d.hex()} {d}\t{build_id}.{product_id}.{count}"

            f.write(line + '\n')
            print(line)

filepath = "Rich_Header"
savepath = filepath + "(Decoded)"
rich_tag = bytes.fromhex("52696368")  # Rich
dans_tag = bytes.fromhex("44616E53")  # DanS

chunks = read_chunks(filepath)
rich_idx, key_idx = find_rich_and_key(chunks, rich_tag)
key = chunks[key_idx]

decoded_chunks = decode_chunks(chunks, rich_idx, key, dans_tag)

write_chunks(decoded_chunks, savepath)
write_parse_chunks(decoded_chunks, savepath)