<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');
</style>
<template>
  <div class="container mt-5">
    <!-- 섹션 헤더 -->
    <section class="d-flex justify-content-between align-items-center mb-4 section-header">
      <div>
        <h1 class="fw-bold mb-2 section-title">은행 위치 검색</h1>
        <p class="lead section-subtitle">근처의 은행 위치를 간편하게 검색해보세요</p>
      </div>
    </section>

    <!-- 필터 선택 -->
    <section class="filter-section mb-4">
      <div class="row g-3">
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
            <button @click="searchBanks" class="btn btn-primary btn-search">
              검색
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 지도 -->
    <section class="map-section position-relative">
      <div
        id="map"
        class="rounded"
        style="width: 100%; height: 600px;"
      ></div>

      <!-- 은행 정보 -->
      <div
        v-if="selectedBankInfo"
        class="info-box bg-white p-3 shadow rounded"
      >
        <h5 class="text-black">🏦 {{ selectedBankInfo.place_name }}</h5>
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
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";

const map = ref(null);
const bankMarkers = ref([]);
const provinces = ref([
  "서울",
  "부산",
  "대구",
  "인천",
  "광주",
  "대전",
  "울산",
  "세종",
  "경기도",
  "강원도",
  "충청북도",
  "충청남도",
  "전라북도",
  "전라남도",
  "경상북도",
  "경상남도",
  "제주도",
]);
const cities = ref([]);
const selectedProvince = ref("");
const selectedCity = ref("");
const selectedBank = ref("");
const selectedBankInfo = ref(null);

const businessHours = computed(() => {
  return "평일 오전 9시 ~ 오후 4시";
});

const fetchCities = () => {
  const cityData = {
  서울: ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구"],
  부산: ["중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "해운대구", "사하구"],
  대구: ["중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"],
  인천: ["중구", "동구", "미추홀구", "연수구", "남동구", "부평구", "계양구", "서구", "강화군", "옹진군"],
  광주: ["동구", "서구", "남구", "북구", "광산구"],
  대전: ["동구", "중구", "서구", "유성구", "대덕구"],
  울산: ["중구", "남구", "동구", "북구", "울주군"],
  세종: ["세종시"],
  경기도: ["수원시", "성남시", "고양시", "용인시", "부천시", "안산시", "안양시", "남양주시", "화성시", "평택시"],
  강원도: ["춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군", "영월군"],
  충청북도: ["청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군"],
  충청남도: ["천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군"],
  전라북도: ["전주시", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군"],
  전라남도: ["목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군"],
  경상북도: ["포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시"],
  경상남도: ["창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군"],
  제주도: ["제주시", "서귀포시"]
  };
  cities.value = cityData[selectedProvince.value] || [];
  selectedCity.value = "";
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
      "//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=80d830a065cca6f44b1812e2f0679579&libraries=services";

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

    kakao.maps.event.addListener(marker, "click", () => {
      selectedBankInfo.value = bank;
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
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');

body {
  font-family: 'Roboto', 'Open Sans', sans-serif;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-family: 'Roboto', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #343a40;
}

.section-subtitle {
  font-family: 'Open Sans', sans-serif;
  font-weight: 400;
  color: #6c757d;
}

.filter-section .form-label {
  font-family: 'Roboto', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  color: #343a40;
}

#map {
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.info-box {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 300px;
  z-index: 1000;
  font-family: 'Open Sans', sans-serif;
}

.btn-search {
  height: 38px;
  color: white;
  background-color: #007bff;
  border: none;
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
}

.btn-search:hover {
  background-color: #0056b3;
}
</style>