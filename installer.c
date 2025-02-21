#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <curl/curl.h>

#define OWNER "Syntaxerrorontop"
#define REPO "GamesManager"
#define TOKEN "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"
#define TARGET_VERSION "3.11.7"

size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    return fwrite(ptr, size, nmemb, stream);
}

void download_private_repo() {
    CURL *curl;
    FILE *fp;
    CURLcode res;
    char url[256];
    char auth_header[512];
    
    snprintf(url, sizeof(url), "https://api.github.com/repos/%s/%s/zipball/main", OWNER, REPO);
    snprintf(auth_header, sizeof(auth_header), "Authorization: token %s", TOKEN);
    
    curl = curl_easy_init();
    if (curl) {
        fp = fopen("sourcecode.zip", "wb");
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, auth_header);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
        fclose(fp);
        if (res == CURLE_OK) {
            printf("Download complete: sourcecode.zip\n");
        } else {
            printf("Download failed: %s\n", curl_easy_strerror(res));
        }
    }
}

void install_requirements() {
    printf("Installing dependencies...\n");
    system("python -m pip install -r requirements.txt");
}

void install_playwright() {
    printf("Installing Playwright...\n");
    system("playwright install");
}

int main() {
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        perror("getcwd error");
        return 1;
    }
    printf("Current directory: %s\n", cwd);
    
    download_private_repo();
    
    install_requirements();
    install_playwright();
    
    return 0;
}
