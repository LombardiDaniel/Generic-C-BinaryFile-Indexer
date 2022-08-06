registro tmp;
char byteBuffer;
std::string strBuffer;

while (fread(&tmp, REG_NO_STR_SIZE, 1, fp)) {

    log("\n[INFO][READ]::regSize:       %lu\n", tmp.size);
    log("[INFO][READ]::valid:         %lu\n", tmp.valid);
    log("[INFO][READ]::ID:            %u\n", tmp.ID);
    log("[INFO][READ]::CATEGORIA:     %u\n", tmp.categoria);
    log("[INFO][READ]::PRECO:         %.2f\n", tmp.preco);

    size_t strBytesMax = tmp.size - (REG_NO_STR_SIZE);
    log("[INFO][READ]::strBytesMax:   %ld\n", strBytesMax);

    if (tmp.ID != requestID || !tmp.valid) {
        tmp = registro(); // = {0}; // ~> zera a struct
        fseek(fp, +strBytesMax, SEEK_CUR); // pula para o próximo registro
        continue;
    }

    size_t counter = 0;
    tmp.nome = std::string();
    while (counter++ < strBytesMax) // reads string
        if (fread(&byteBuffer, sizeof(char), 1, fp))
            tmp.nome.push_back(byteBuffer);

    size_t nomeLen = tmp.nome.length();

    printf("Reg Found:\n");
    printRegistro(tmp);

    printf("Data input: (type \"0\" to keep original)\n");
    printf("\tNUMERO CATEGORIA: ");
    std::cin.ignore();
    getline(std::cin, strBuffer);
    if (atoi(strBuffer.c_str()) != 0) {
        tmp.categoria = atoi(strBuffer.c_str());
        log("[INFO][EDIT]::categoria altered::%d\n", tmp.categoria);
    }

    printf("\tNOME: ");
    // std::cin.ignore();
    getline(std::cin, strBuffer);
    if (strBuffer.compare("0") != 0) {
        tmp.nome = strBuffer;
        nomeLen = tmp.nome.length();
        log("[INFO][EDIT]::name altered::");
        log(tmp.nome);
        log("[INFO][EDIT]::nomeLen: %d\n", nomeLen);
    }

    printf("\tPRECO: ");
    getline(std::cin, strBuffer);
    if (strBuffer.compare("0") != 0) {
        tmp.preco = atof(strBuffer.c_str());
        log("[INFO][EDIT]::preco altered::%.2f\n", tmp.preco);
    }

    std::fseek(fp, - tmp.size, SEEK_CUR); // volta pro inicio do registro

    // *** ATÉ AQUI TA CERTO ***

    // long unsigned newSize = sizeof(registro) - (sizeof(std::string) + strBytesMax) + newNomeLen;
    size_t oldSize = tmp.size;
    size_t newSize = REG_NO_STR_SIZE + nomeLen;
    long long int sizeDiff = oldSize - newSize;
    if (newSize <= oldSize) {
        // inline insert
        log("[INFO][EDIT]:: keeping size: Old=%d, New=%d\n", oldSize, newSize);

        log("\n[INFO][EDIT]::regSize:       %lu\n", tmp.size);
        log("[INFO][EDIT]::valid:         %lu\n", tmp.valid);
        log("[INFO][EDIT]::ID:            %u\n", tmp.ID);
        log("[INFO][EDIT]::CATEGORIA:     %u\n", tmp.categoria);
        log("[INFO][EDIT]::PRECO:         %.2f\n", tmp.preco);
        log("[INFO][EDIT]::NOME:          ");
        log(tmp.nome);

        for (size_t i = 0; i < sizeDiff; i++)
            tmp.nome.push_back('\0');

        // fwrite(&tmp, REG_NO_STR_SIZE, 1, fp);
        // fwrite(tmp.nome.c_str(), tmp.nome.length(), 1, fp);
        // fwrite("\0", 1, sizeDiff, fp);

        auto status = writeReg(fp, tmp);
        if (!status) {
            log("%s[ERROR][WRITE]::status writeReg: %d%s", RED, status, WHITE);
            printf("[ERROR][WRITE]::status writeReg: %d", status);
            return 1;
        }

        break;

    } else {
        // DOES NOT WORK CORRECTLY
        log("[INFO][EDIT]::page break\n");

        // pode salvar o offset em algum lugar né, pra pular direto, ai faz tipo um Link Register pra voltar
        // SIM:: vamos fzer isso aqui:
        unsigned long start = (unsigned long) std::ftell(fp);
        std::fseek(fp, 0, SEEK_END);
        unsigned long end = (unsigned long) std::ftell(fp);
        unsigned long offset = end - start;

        std::fseek(fp, -offset, SEEK_END);

        _registroEdit tmpEdit = _registroEdit();
        tmpEdit.size = tmpEdit.size;
        tmpEdit.ID = tmp.ID;
        tmpEdit.valid = tmpEdit.valid;

        if (DEBUG) {
            fread(&tmpEdit, REG_NO_STR_SIZE, 1, fp);
            log("%s[INFO][EDIT]::BEFORE_WRITE::%s\n", RED, WHITE);
            log("[INFO][EDIT]::regSize:       %lu\n", tmpEdit.size);
            log("[INFO][EDIT]::valid:         %lu\n", tmpEdit.valid);
            log("[INFO][EDIT]::ID:            %u\n", tmpEdit.ID);
            log("[INFO][EDIT]::[TMP]CATEGORIA:     %u\n", tmp.categoria);
            log("[INFO][EDIT]::[TMP]PRECO:         %.2f\n", tmp.preco);
            log("[INFO][EDIT]::NAME(NEW):     ");
            log(tmp.nome);

            std::fseek(fp, - REG_NO_STR_SIZE, SEEK_CUR);
        }

        tmp.valid = 0;
        auto oldID = tmp.ID;
        tmp.ID = ++offset;
        log("[INFO][EDIT]::offset: %lu\n", offset);

        fwrite(&tmp, FIRST_FIELDS_SIZE, 1, fp); // salva os dados novos e invalidez na pos do reg atual (antigo)
        std::fseek(fp, - FIRST_FIELDS_SIZE, SEEK_CUR);

        if (DEBUG) {
            fread(&tmp, REG_NO_STR_SIZE, 1, fp);
            log("\n%s[INFO][EDIT]::AFTER INVALIDATION::%s\n", RED, WHITE);
            log("[INFO][EDIT]::regSize:       %lu\n", tmp.size);
            log("[INFO][EDIT]::valid:         %lu\n", tmp.valid);
            log("[INFO][EDIT]::ID:            %u\n", tmp.ID);
            log("[INFO][EDIT]::CATEGORIA:     %u\n", tmp.categoria);
            log("[INFO][EDIT]::PRECO:         %.2f\n", tmp.preco);
            log("[INFO][EDIT]::NAME(NEW):     ");
            log(tmp.nome);

            std::fseek(fp, - REG_NO_STR_SIZE, SEEK_CUR);
        }

        tmp.ID = oldID;
        tmp.valid = 1;
        tmp.size = REG_NO_STR_SIZE + tmp.nome.length();

        // bloco zuado testar dpois::
        // fwrite(&tmp, sizeof(size_t) + 8, 1, fp); // re.size + reg.valid + reg.id (neste caso, id na vdd eh o offset, que pode ser utilizado na busca)
        // OS ERROS TEM HAVER C ALINHAMENTO DE MEMORIA DO COMPILER -> TESTAR SEM E TESTAR COM
        // fwrite(&tmp, FIRST_FIELDS_SIZE, 1, fp);

        log("\n[INFO][EDIT]::regSize:       %lu\n", tmp.size);
        log("[INFO][EDIT]::valid:         %lu\n", tmp.valid);
        log("[INFO][EDIT]::ID:            %u\n", tmp.ID);
        log("[INFO][EDIT]::CATEGORIA:     %u\n", tmp.categoria);
        log("[INFO][EDIT]::PRECO:         %.2f\n", tmp.preco);
        // Navigate to EOF and append new reg
        std::fseek(fp, 0, SEEK_END);

        auto status = writeReg(fp, tmp);
        if (!status) {
            log("%s[ERROR][EDIT]::status writeReg: %d%s", RED, status, WHITE);
            printf("[ERROR][EDIT]::status writeReg: %d", status);
            return 1;
        }

        if (DEBUG) {
            fread(&tmp, REG_NO_STR_SIZE, 1, fp);
            log("\n%s[INFO][EDIT]::AFTER_WRITE::%s\n", RED, WHITE);
            log("[INFO][EDIT]::regSize:       %lu\n", tmp.size);
            log("[INFO][EDIT]::valid:         %lu\n", tmp.valid);
            log("[INFO][EDIT]::ID:            %u\n", tmp.ID);
            log("[INFO][EDIT]::CATEGORIA:     %u\n", tmp.categoria);
            log("[INFO][EDIT]::PRECO:         %.2f\n", tmp.preco);

            int strBytesMax = tmp.size - REG_NO_STR_SIZE;
            size_t counter = 0;
            tmp.nome = std::string();
            while (counter++ < strBytesMax) // reads string
                if (fread(&byteBuffer, sizeof(char), 1, fp))
                    tmp.nome.push_back(byteBuffer);

            log("[INFO][EDIT]::NAME(NEW):     ");
            log(tmp.nome);

            std::fseek(fp, - oldSize, SEEK_CUR);
        }

        break;
    }

}
