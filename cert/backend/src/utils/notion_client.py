from datetime import datetime
import os
import aiohttp
from typing import Optional, Dict, Any

class NotionClient:
    """Notion API 클라이언트 (직접 HTTP 호출)"""
    
    def __init__(self):
        self.notion_token = os.getenv("NOTION_API_KEY")
        # 데이터베이스 ID들을 환경 변수로 관리
        self.databases = {
            "project_history": os.getenv("NOTION_PROJ_DB_ID"),
            "certificate_requests": os.getenv("NOTION_CERT_DB_ID")
        }
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    async def verify_user_participation(
        self,
        user_name: str,
        course_name: str,
        season: int
    ) -> Dict[str, Any]:
        """사용자 참여 이력 확인 (빌더/러너 확인)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases['project_history']}/query"
                
                payload = {
                    "filter": {
                        "and": [
                            {
                                "property": "기수",
                                "multi_select": {   # NOTE: select, multi_select 등 속성 값 명확하게
                                    "contains": f"{season}기"
                                }
                            },
                            {
                                "property": "이름",
                                "title": {      # NOTE: title, rich_text 은 부분 문자열 검색가능
                                    "contains": course_name
                                }
                            }
                        ]
                    }
                }
                
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["results"]:
                            if len(data["results"]) > 1:
                                print(f"다 수{(len(data['results']))}의 결과가 검색되었습니다.")
                            project = data["results"][0]
                            properties = project.get("properties", {})
                            
                            # 빌더, 러너, 수료자, 이탈자 확인
                            builders = properties.get("빌더", {}).get("multi_select", [])
                            runners = properties.get("러너", {}).get("multi_select", [])
                            completers = properties.get("수료자", {}).get("rich_text", [])
                            dropouts = properties.get("이탈자", {}).get("multi_select", [])
                            
                            builder_names = [b.get("name", "") for b in builders]
                            runner_names = [r.get("name", "") for r in runners]
                            completer_names = [c.get("plain_text", "") for c in completers]
                            dropout_names = [d.get("name", "") for d in dropouts]
                            
                            # 1. 사용자가 빌더, 러너, 수료자 중 하나에 있는지 확인
                            user_role = None
                            if user_name in builder_names:
                                user_role = "BUILDER"
                            elif user_name in runner_names:
                                user_role = "LEARNER"
                            
                            # 2. 사용자가 이탈자에 있는지 확인
                            if user_name in dropout_names:
                                print(f"사용자 {user_name}이(가) 이탈자 목록에 있습니다.")
                                return {
                                    "found": False,
                                    "user_role": None,
                                    "project_data": None,
                                    "reason": "이탈자"
                                }
                            
                            # 3. 사용자가 참여자 목록에 있는지 확인
                            if user_role is None:
                                print(f"사용자 {user_name}이(가) 참여자 목록에 없습니다.")
                                return {
                                    "found": False,
                                    "user_role": None,
                                    "project_data": None,
                                    "reason": "참여자 아님"
                                }
                            
                            print(f"사용자 {user_name} 검증 성공: {user_role}")
                            return {
                                "found": True,
                                "project_id": project.get("id"),
                                "user_role": user_role,
                                "project_data": project
                            }
                    
                    return {"found": False, "user_role": None, "project_data": None}
                    
        except Exception as e:
            print(f"사용자 참여 이력 확인 중 오류: {e}")
            return {"found": False, "user_role": None, "project_data": None}
    
    async def create_certificate_request(
        self,
        certificate_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """수료증 신청 기록 생성 (수료증 DB에)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/pages"
                
                payload = {
                    "parent": {
                        "database_id": self.databases["certificate_requests"]
                    },
                    "properties": {
                        "Name": {
                            "title": [
                                {
                                    "text": {
                                        "content": certificate_data["applicant_name"]
                                    }
                                }
                            ]
                        },
                        "Issue Date": {
                            "date": {
                                "start": datetime.now().strftime("%Y-%m-%d")
                            }
                        },
                        "Recipient Email": {
                            "email": certificate_data["recipient_email"]
                        },
                        "Course Name": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": certificate_data["course_name"]
                                    }
                                }
                            ]
                        },
                        "Season": {
                            "select": { 
                                "name": f"{certificate_data['season']}기"
                            }
                        },
                        "Certificate Status": {
                            "status": {
                                "name": "Pending"
                            }
                        }
                    }
                }
                
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"수료증 신청 생성 오류: {response.status}")
                        error_text = await response.text()
                        print(f"오류 내용: {error_text}")
                    return None
                    
        except Exception as e:
            print(f"수료증 신청 생성 중 오류: {e}")
            return None
    
    async def update_certificate_status(
        self,
        page_id: str,
        status: str,
        certificate_number: str = None,
        role: str = None
    ) -> bool:
        """수료증 상태 업데이트"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/pages/{page_id}"
                
                update_data = {
                    "properties": {
                        "Certificate Status": {
                            "status": {
                                "name": status
                            }
                        }
                    }
                }
                
                # 수료증 번호 추가
                if certificate_number:
                    update_data["properties"]["Certificate Number"] = {
                        "rich_text": [
                            {
                                "text": {
                                    "content": certificate_number
                                }
                            }
                        ]
                    }
                
                # 역할 업데이트
                if role:
                    update_data["properties"]["Role"] = {
                        "select": {
                            "name": role
                        }
                    }
                
                async with session.patch(url, headers=self.headers, json=update_data) as response:
                    if response.status == 200:
                        return True
                    else:
                        print(f"상태 업데이트 오류: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"상태 업데이트 중 오류: {e}")
            return False

    async def get_database_structure(self, database_type: str = "project_history") -> Optional[Dict[str, Any]]:
        """데이터베이스 구조 조회 (디버깅용)"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/databases/{self.databases[database_type]}"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"데이터베이스 구조 조회 오류: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"데이터베이스 구조 조회 중 오류: {e}")
            return None
        
