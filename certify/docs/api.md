# API 명세서

## 수료증 발급 요청
사용자가 입력한 정보를 통해 수료증 발급 파이프라인에 수료증을 요청합니다.

HTTP Method : POST  
URL : https://cert.pseudolab-devfactory/certs/create

### Request
#### Header 
| 이름 | 내용        | 필수             |
|--------|----------------|------------------|
| Content-Type   | `application/json`   | O           |

#### Body
| 이름            | 타입      | 설명               |  필수 |
| ------------- | ------- | ---------------- | :-: |
| applicant_name          | String  | 신청자 이름           |  O  |
| recipient_email         | String  | 수료자 이메일          |  O  |
| course_name     | String  | 과정명        |  O  |
| cohort        | Int  | 활동기수(예: `10`) |  O  |


### Response

### Error Code
| HTTP Status | Error Code | Message | 설명 |
|-------------|------------|---------|------|
| **200 OK** | - | 수료증이 성공적으로 발급되었습니다. | 정상 처리 완료 |
| **404 Not Found** | CS0002 | 수료 이력이 확인되지 않습니다. | 사용자의 수료 이력이 존재하지 않음 |
| **500 Internal Server Error** | CS0003 | 발급 처리 중 오류가 발생했습니다. | 수료증 생성, 이메일 발송 등 내부 파이프라인 오류 |

#### 성공시 
| 이름      | 타입     | 설명                      |
| ------- | ------ | ----------------------- |
| status  | String | `"200"` 또는 `"404"` |
| message | String | 결과 메세지                  |
| data | Object | 수료증 데이터 |
| id | Int | 수료증 신청 ID |
| certificate_number | String | 수료증 번호 |

#### 실패시 

| 이름      | 타입     | 설명                      |
| ------- | ------ | ----------------------- |
| status  | String | `"404"` |
| error_code | String | 에러 코드 |
| message | String | 결과 메세지                  |

### Example

#### Request
```
{
  "name": "홍길동",
  "email": "gildong@example.com",
  "cohort": "10",
  "course_name": "MLOps Bootcamp"
}

```



### Response Examples

#### 성공 응답
```json
{
  "status": "success",
  "message": "수료증이 성공적으로 발급되었습니다. 🚀\n메일함을 확인해보세요.",
  "data": {
    "id": 1,
    "certificate_number": "CERT-001"
    ...
  }
}
```



#### 실패 응답 - 수료 이력 없음 (404)
```json
{
  "status_code": 404,
  "detail": {
    "status": "fail",
    "error_code": "CS0002",
    "message": "수료 이력이 확인되지 않습니다."
  }
}
```

#### 실패 응답 - 서버 오류 (500)
```json
{
  "status_code": 500,
  "detail": {
    "status": "fail",
    "error_code": "CS0003",
    "message": "발급 처리 중 오류가 발생했습니다."
  }
}
```