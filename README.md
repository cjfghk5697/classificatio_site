# classification_site
BackEnd : DRF <br/>
FrontEnd : React, TailwindCSS <br/>
AI : Pytorch

[데이터](https://dacon.io/competitions/official/235894/overview/description)

## 요약
간단히 모델 변경만으로 사이트를 특정 모델에 맞게 바꿀수 있다. pytorch, DRF와 React를 연동하여 사이트를 만들었다. 예측 결과 중 가장 확률 이 높은 5개는 비교가 가능하도록 예측 결과 페이지에서 확인 할 수 있도록하였다.

![image](https://user-images.githubusercontent.com/80466735/184155543-76c2fe98-8970-45f4-8815-ccd9505fde3f.png)

_img.1 시작페이지_

![image](https://user-images.githubusercontent.com/80466735/186406340-cd8be29b-db75-45da-9c16-fefbce343fad.png)

_img.2 React 분류 결과_

![image](https://user-images.githubusercontent.com/80466735/184157151-3d77de3b-6758-4546-97ce-df03bd20689f.png)

_img.3 DRF 분류 결과_


## 사용법

- 코드 가져오기
```
git clone https://github.com/cjfghk5697/classification_site.git
```

- 코드 실행
 첫번째 줄은 DRF 실행코드 두번째 줄은 react 실행코드다.
```
python3 /workspace/drf_disease/manage.py migrate && python3 /workspace/drf_disease/manage.py runserver 0.0.0.0:8000
npm install && npm start
```

- 다른 모델 적용
inference.py에서 수정해야할 부분이 있다.
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
http-common.js에서 코드를 수정해야한다. baseURL부분을 수정하면된다.
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
frontend에서 뒤에 id를 추가하면된다. 위에 이미지에서 이미지마다 id가 적혀있다. 그 id를 주소 맨 뒤에 입력하면 예측하도록 되어있다.

## 문제점 및 유의사항
- 모델 불러오는 속도가 매우 느림
  apps.py에 모델을 넣어 다시 가져오지 않고 재사용하도록 수정했다. 하지만 goorm ide를 이용해 개발 중이어서인지 모르지만 속도가 느리다. 만약 이 코드를 사용할때 backend는 좋은 GPU를 적용하길 바란다. 혹은 모델을 mobileNet과 같은 가볍고 FLOP이 좋은 모델을 사용해야한다. 그래서 오래 예측이 안되더라도 걱정말고 대기하면 나온다. (대략 2분)

- 버전 문제
  goorm ide 버전이 낮아 못한 것들이 있다. 예시로 pytorch 같은 경우 efficientNet 모델이 적용되지 않은 버전이다. 만약 efficientNet 모델을 사용할 거라면 더 높은 버전으로 수정하길 바란다.

- 예측 확률 문제
  예측 결과에서 이유 없이 확률 바를 넣은 게 아니다. 적절한 거부옵션을 할 수 있기 위해서 만들었다. 이뿐만 아니라 만약 확률이 다 똑같이 나온다면 그 예측 결과에 신뢰도가 떨어지기에 이런걸 방지하기 위해 넣었다.
