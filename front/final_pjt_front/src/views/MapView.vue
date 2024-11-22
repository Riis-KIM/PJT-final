<template>
  <div class="container mt-5">
    <!-- 섹션 헤더 -->
    <section class="d-flex justify-content-between align-items-center mb-4 section-header">
      <div>
        <h1 class="fw-bold mb-2 section-title">🏦 은행 위치 검색</h1>
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
const selectedBankInfo = ref(null);

const businessHours = computed(() => {
  return "평일 오전 9시 ~ 오후 4시";
});

const fetchCities = () => {
  const cityData = {
    서울특별시: ["종로구", "중구", "용산구", "성동구", "광진구"],
    부산광역시: ["중구", "서구", "동구", "영도구", "부산진구"],
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
.section-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 2rem;
  color: #343a40; /* 검은색 */
}

.section-subtitle {
  color: #6c757d; /* 회색 */
}

.filter-section .form-label {
  font-size: 0.9rem;
  font-weight: bold;
  color: #343a40; /* 검은색 */
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
}

.btn-search {
  height: 38px;
  color: white;
  background-color: #007bff;
  border: none;
}

.btn-search:hover {
  background-color: #0056b3;
}
</style>
