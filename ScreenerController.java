package com.resumescreener.resume_screener;

import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@CrossOrigin(origins = "*")
public class ScreenerController {

    private final String ML_SERVICE_URL = "http://localhost:8000/screen";

    @PostMapping("/screen")
    public ResponseEntity<?> screenResumes(
            @RequestParam("jd") MultipartFile jd,
            @RequestParam("resumes") List<MultipartFile> resumes
    ) throws IOException {

        // Build multipart request to ML service
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

        // Add JD file
        ByteArrayResource jdResource = new ByteArrayResource(jd.getBytes()) {
            @Override
            public String getFilename() {
                return jd.getOriginalFilename();
            }
        };
        body.add("jd", jdResource);

        // Add resume files
        for (MultipartFile resume : resumes) {
            ByteArrayResource resumeResource = new ByteArrayResource(
                resume.getBytes()) {
                @Override
                public String getFilename() {
                    return resume.getOriginalFilename();
                }
            };
            body.add("resumes", resumeResource);
        }

        // Send request to ML service
        HttpEntity<MultiValueMap<String, Object>> requestEntity =
            new HttpEntity<>(body, headers);

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<Object> mlResponse = restTemplate.postForEntity(
            ML_SERVICE_URL, requestEntity, Object.class
        );

        return ResponseEntity.ok(mlResponse.getBody());
    }

    @GetMapping("/health")
    public ResponseEntity<?> health() {
        return ResponseEntity.ok("Spring Boot is running!");
    }
}
