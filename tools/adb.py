
"""
The transport layer deals in "messages", which consist of a 24 byte
header followed (optionally) by a payload.  The header consists of 6
32 bit words which are sent across the wire in little endian format.
struct message {
    unsigned command;       /* command identifier constant      */
    unsigned arg0;          /* first argument                   */
    unsigned arg1;          /* second argument                  */
    unsigned data_length;   /* length of payload (0 is allowed) */
    unsigned data_crc32;    /* crc32 of data payload            */
    unsigned magic;         /* command ^ 0xffffffff             */
};

#define A_SYNC 0x434e5953
#define A_CNXN 0x4e584e43 #CONNECT?
#define A_OPEN 0x4e45504f #OPEN
#define A_OKAY 0x59414b4f
#define A_CLSE 0x45534c43
#define A_WRTE 0x45545257

"""

def forgeADBPacket(command, arg0, arg1, data):
    magic = int.from_bytes(command, 'little') ^ 0xFFFFFFFF

    _format =  b'<6I'
    command = int.from_bytes(command, 'little')
    if isinstance(arg0, bytes):
        arg0 = int.from_bytes(arg0, 'little')
    if isinstance(arg1, bytes):
        arg1 = int.from_bytes(arg1, 'little')
    checksum = 0 # checksums are not required since ADB version 2

    packet = struct.pack(_format, command, arg0, arg1, len(data), checksum, magic)
    print('Forged ADB packet', packet, len(packet))
    return packet + data

def parseADBHeader(data):
    _format =  b'<6I'
    command, arg0, arg1, length, checksum, magic = struct.unpack(_format, data)
    command = command.to_bytes(6, 'little')
    arg0 = arg0.to_bytes(6, 'little')
    arg1 = arg1.to_bytes(6, 'little')
    print('PARSE ADB HEADER COMMAND', command)
    return command, arg0, arg1

def ADBHandler(input_buff, data):
    command = data[:4]
    payload = data[24:]
    parsed_header = parseADBHeader(data[:24])
    
    print('ADBHandler->command', parsed_header[0])
    print('ADBHandler->arg0', parsed_header[1])
    print('ADBHandler->arg1', parsed_header[2])
    print('ADBHandler->payload', payload)

    print('Parsed packet', parsed_header)
    if command == b'CNXN': # CNXN
        print('CNXD REQUEST')
        answer = b"CNXN\x01\x00\x00\x01\x00\x00\x10\x00\x10\x01\x00\x00\xa1f\x00\x00\xbc\xb1\xa7\xb1"
        print('HEADER_LEN', len(answer))
        answer += b'device::ro.product.name=sdk_gphone_x86_64_arm64;ro.product.model=sdk_gphone_x86_64_arm64;ro.product.device=generic_x86_64_arm64;features=sendrecv_v2_brotli,remount_shell,sendrecv_v2,abb_exec,fixed_push_mkdir,fixed_push_symlink_timestamp,abb,shell_v2,cmd,ls_v2,apex,stat_v2\0'
        print('hexdump:', answer.hex())
        return answer    
    else:
        print('GOT ANOTHER PACKET THAN CNXN')
        exit(0)

def generateStringsForDevice(product_name, product_model, product_device, features="sendrecv_v2_brotli,remount_shell,sendrecv_v2,abb_exec,fixed_push_mkdir,fixed_push_symlink_timestamp,abb,shell_v2,cmd,ls_v2,apex,stat_v2"):
    bindata = b"CNXN\x01\x00\x00\x01\x00\x00\x10\x00\x10\x01\x00\x00\xa1f\x00\x00\xbc\xb1\xa7\xb1"
    bindata += (f"device::ro.product.name={product_name};ro.product.model={product_model};ro.product.device={product_device};features={features}").encode('UTF-8')
    print("0x"+bindata.hex())
    print(f"""Android Debug Bridge (ADB):
    Name: {product_name}
    Model: {product_model}
    Device: {product_device}""")
    if features and len(features):
        print("    Features:")
    for feature in features.split(','):
        print("      "+feature)
