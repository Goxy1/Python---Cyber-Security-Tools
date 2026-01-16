import hashlib

type_of_hash = str(input('Enter the type of hash you want to brute-force:'))
file_path = str(input('Enter path to the file to bruteforce with: '))
hash_to_decrypt = str(input('Enter hash value to bruteforce: '))

with open(file_path, 'r') as file:
    for line in file.readlines():
        if type_of_hash == 'md5':
            hash_object = hashlib.md5(line.strip().encode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Found MD5 Password: ' + line.strip())
                exit(0)

        if type_of_hash == 'sha1':
            hash_object = hashlib.sha1(line.strip().ecnode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Found SHA1 password: ' + line.strip())
                exit(0)

    print('Password not found in File')