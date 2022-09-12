# classification_site

[데이터](https://dacon.io/competitions/official/235894/overview/description)

## 요약
간단히 모델 변경만으로 사이트를 특정 모델에 맞게 바꿀수 있습니다. 사이트의 강점은 의료진단과 같은 인공지능에 적합하게 만들었습니다. 왜 이 진단이 맞는지 XAI 기법 중 Grad CAM으로 설 득력을 높이고 예측 결과 중 가장 확률 이 높은 5개를 비교가 가능하도록 예측 결과 페이지에서 확인 할 수 있도록 했습니다.

![image](https://user-images.githubusercontent.com/80466735/184155543-76c2fe98-8970-45f4-8815-ccd9505fde3f.png)

_img.1 시작페이지_

![image](https://user-images.githubusercontent.com/80466735/189580356-4eb758f2-de0a-4b84-8bae-791a84c0d1ee.png)

_img.2 React 분류 결과_

![image](https://user-images.githubusercontent.com/80466735/189580569-8ad5aac0-8df8-4f06-bcb0-e862f588d07a.png)

_img.3 DRF 분류 결과_


## 사용법

- 코드 가져오기
```
git clone https://github.com/cjfghk5697/classification_site.git
```

- 코드 실행
 첫번째 줄은 DRF 실행코드 두번째 줄은 react 실행코드입니다.
```
# DRF 실행코드
python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000

# 리액트 실행코드
npm install && npm start
```
- 패키지 다운

```
pip install -r requirements.txt
```


- 다른 모델 적용
inference.py에서 수정해야할 부분이 있습니다.
 1. 모델 가져올때
```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Network().to(device)
model.load_state_dict(torch.load('(경로)'), strict=False)
```
 2. 라벨 변경할때
```python
train_y = pd.read_csv('(경로)')
train_labels = train_y["label"]
```

- 주소 변경
http-common.js에서 코드를 수정해야합니다. baseURL부분을 수정하면됩니다.
```javascript
import axios from "axios";
export default axios.create({
  baseURL: "(주소)",
  headers: {
    'Accept': 'application/json',
    "Content-type": "application/json"
  }
});
```
- 예측방법
frontend에서 뒤에 id를 추가하면됩니다. 위에 이미지에서 이미지마다 id가 적혀있습니다. 그 id를 주소 맨 뒤에 입력하면 예측하도록 되어있습니다.

