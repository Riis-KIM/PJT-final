<template>
  <div class="container mt-5">
    <h1 class="fw-bold text-center mb-4 text-primary">🏦 은행 위치 검색</h1>

    <!-- 필터 선택 -->
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <label for="province" class="form-label fw-bold">시/도</label>
        <select
          id="province"
          class="form-select"
          v-model="selectedProvince"
          @change="fetchCities"
        >
          <option value="" disabled selected>시/도 선택</option>
          <option v-for="province in provinces" :key="province" :value="province">
            {{ province }}
          </option>
        </select>
      </div>
      <div class="col-md-3">
        <label for="city" class="form-label fw-bold">시/구/군</label>
        <select
          id="city"
          class="form-select"
          v-model="selectedCity"
          :disabled="!cities.length"
        >
          <option value="" disabled selected>시/구/군 선택</option>
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <label for="bank" class="form-label fw-bold">은행</label>
        <div class="input-group">
          <input
            id="bank"
            type="text"
            class="form-control"
            v-model="selectedBank"
            placeholder="은행 이름 입력"
          />
          <button @click="searchBanks" class="btn btn-primary">검색</button>
        </div>
      </div>
    </div>

    <!-- 지도 -->
    <div id="map-container" class="position-relative" style="height: 600px; border: 1px solid #ddd; border-radius: 5px;">
      <!-- 지도 -->
      <div
        id="map"
        style="width: 100%; height: 100%; border-radius: 5px;"
      ></div>

      <!-- 은행 정보 -->
      <div
        v-if="selectedBankInfo"
        class="position-absolute bg-white p-3 shadow rounded"
        style="top: 10px; right: 10px; width: 300px; z-index: 1000;"
      >
        <h5 class="text-primary">🏦 {{ selectedBankInfo.place_name }}</h5>
        <p>
          <strong>도로명 주소:</strong>
          {{ selectedBankInfo.road_address_name || "정보 없음" }}
        </p>
        <p>
          <strong>지번 주소:</strong>
          {{ selectedBankInfo.address_name || "정보 없음" }}
        </p>
        <p><strong>전화번호:</strong> {{ selectedBankInfo.phone || "정보 없음" }}</p>
        <p><strong>영업시간:</strong> {{ businessHours }}</p>
        <button
          class="btn btn-secondary w-100 mt-2"
          @click="selectedBankInfo = null"
        >
          닫기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";

const map = ref(null);
const bankMarkers = ref([]);
const provinces = ref([
  "서울특별시",
  "부산광역시",
  "대구광역시",
  "인천광역시",
  "광주광역시",
  "대전광역시",
  "울산광역시",
  "세종특별자치시",
  "경기도",
  "강원도",
  "충청북도",
  "충청남도",
  "전라북도",
  "전라남도",
  "경상북도",
  "경상남도",
  "제주특별자치도",
]);
const cities = ref([]);
const selectedProvince = ref("");
const selectedCity = ref("");
const selectedBank = ref("");
const selectedBankInfo = ref(null); // 선택된 은행 정보를 저장

// 기본 영업시간
const businessHours = computed(() => {
  // 특정 조건에 따라 변경 가능
  return "평일 오전 9시 ~ 오후 4시";
});

const fetchCities = () => {
  const cityData = {
  서울특별시: [
    "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구",
    "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구",
    "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"
  ],
  부산광역시: [
    "중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "해운대구",
    "사하구", "금정구", "강서구", "연제구", "수영구", "사상구", "기장군"
  ],
  대구광역시: [
    "중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"
  ],
  인천광역시: [
    "중구", "동구", "미추홀구", "연수구", "남동구", "부평구", "계양구", "서구",
    "강화군", "옹진군"
  ],
  광주광역시: [
    "동구", "서구", "남구", "북구", "광산구"
  ],
  대전광역시: [
    "동구", "중구", "서구", "유성구", "대덕구"
  ],
  울산광역시: [
    "중구", "남구", "동구", "북구", "울주군"
  ],
  세종특별자치시: [
    "세종특별자치시"
  ],
  경기도: [
    "수원시", "고양시", "용인시", "성남시", "부천시", "안산시", "안양시", "남양주시", 
    "화성시", "평택시", "의정부시", "파주시", "시흥시", "김포시", "광주시", "광명시",
    "군포시", "오산시", "이천시", "안성시", "의왕시", "양주시", "구리시", "포천시",
    "하남시", "여주시", "양평군", "가평군", "연천군"
  ],
  강원도: [
    "춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군",
    "횡성군", "영월군", "평창군", "정선군", "철원군", "화천군", "양구군", "인제군",
    "고성군", "양양군"
  ],
  충청북도: [
    "청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군",
    "괴산군", "음성군", "단양군"
  ],
  충청남도: [
    "천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시",
    "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"
  ],
  전라북도: [
    "전주시", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군",
    "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"
  ],
  전라남도: [
    "목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군",
    "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군",
    "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"
  ],
  경상북도: [
    "포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시",
    "문경시", "경산시", "군위군", "의성군", "청송군", "영양군", "영덕군", "청도군",
    "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"
  ],
  경상남도: [
    "창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시",
    "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군",
    "거창군", "합천군"
  ],
  제주특별자치도: [
    "제주시", "서귀포시"
  ]
};
  cities.value = cityData[selectedProvince.value] || [];
  selectedCity.value = ""; // Reset city when province changes
};

const initMap = () => {
  const container = document.getElementById("map");
  const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 8,
  };
  map.value = new kakao.maps.Map(container, options);
};

const loadKakaoMap = () => {
  if (!window.kakao || !window.kakao.maps) {
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src =
      "//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=80d830a065cca6f44b1812e2f0679579&libraries=clusterer,drawing,services";

    /* global kakao */
    script.addEventListener("load", () => {
      kakao.maps.load(() => {
        initMap();
      });
    });
    document.head.appendChild(script);
  } else {
    initMap();
  }
};

const searchBanks = () => {
  if (!selectedProvince.value || !selectedCity.value || !selectedBank.value) {
    alert("모든 필터를 입력해주세요.");
    return;
  }

  const ps = new kakao.maps.services.Places();

  const query = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`;
  ps.keywordSearch(query, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      displayBanksOnMap(data);
    } else {
      alert("검색 결과가 없습니다.");
    }
  });
};

const displayBanksOnMap = (banks) => {
  // Clear existing markers
  bankMarkers.value.forEach((marker) => marker.setMap(null));
  bankMarkers.value = [];

  banks.forEach((bank) => {
    const position = new kakao.maps.LatLng(bank.y, bank.x);
    const marker = new kakao.maps.Marker({
      position,
      map: map.value,
    });

    const infoWindow = new kakao.maps.InfoWindow({
      content: `<div style="padding:5px;">${bank.place_name}</div>`,
    });

    // 마커 클릭 이벤트 추가
    kakao.maps.event.addListener(marker, "click", () => {
      selectedBankInfo.value = bank; // 선택된 은행 정보 저장
    });

    kakao.maps.event.addListener(marker, "mouseover", () => {
      infoWindow.open(map.value, marker);
    });

    kakao.maps.event.addListener(marker, "mouseout", () => {
      infoWindow.close();
    });

    bankMarkers.value.push(marker);
  });

  if (banks.length) {
    const bounds = new kakao.maps.LatLngBounds();
    banks.forEach((bank) => bounds.extend(new kakao.maps.LatLng(bank.y, bank.x)));
    map.value.setBounds(bounds);
  }
};

onMounted(() => {
  loadKakaoMap();
});
</script>

<style scoped>
#map {
  border-radius: 5px;
}

.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

button {
  padding: 10px 20px;
  border-radius: 5px;
}
</style>
