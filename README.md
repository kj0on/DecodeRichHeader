# DecodeRichHeader
이 프로젝트는 PE 파일의 Rich Header를 추출하고 복호화하여 컴파일 정보(제품 식별자, 빌드 번호, 빌드 프로세스 중 사용 횟수)를 분석하는 도구로 PE 파일을 4바이트 단위로 분할한 뒤 "Rich" 문자열과 xor Key를 찾아 암호화된 메타데이터를 해제하고 복호화된 Rich Header의 내용을 파일형태로 저장한다.
