<template>
  <div>
    <h1>ERROR-LOGGING TOOL</h1>
    <div class="flex w-screen h-screen p-10 space-x-4 overflow-auto text-gray-700">
      <div class="flex flex-col flex-shrink-0bg-gray-200 border border-gray-300">
        <div class="flex items-center justify-between flex-shrink-0 h-10 px-2 border-b border-gray-300 bg-white">
          <span class="block text-sm font-medium bg-red-500">UNRESOLVED</span>
        </div>
        <div class="flex flex-col px-2 pb-2 overflow-auto">
          <div v-for="error in unresolved" :key="error.index">
            <div class="flex flex-row px-2 pb-2 overflow-auto">
              <div class="border border-red-600 text-center w-10">{{ error.code }}</div>
              <div class="border border-red-600 text-center w-96">{{ error.text }}</div>
              </div>
            </div>
          </div>
      </div>
      <div class="flex flex-col flex-shrink-0bg-gray-200 border border-gray-300">
        <div class="flex items-center justify-between flex-shrink-0 h-10 px-2 border-b border-gray-300 bg-white">
          <span class="block text-sm font-medium bg-green-500">RESOLVED</span>
        </div>
        <div class="flex flex-col px-2 pb-2 overflow-auto">
          <div v-for="error in resolved" :key="error.index">
            <div class="flex flex-row px-2 pb-2 overflow-auto">
              <div class="border border-green-600 text-center w-10">{{ error.code }}</div>
              <div class="border border-green-600 text-center w-96">{{ error.text }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-col flex-shrink-0bg-gray-200 border border-gray-300">
        <div class="flex items-center justify-between flex-shrink-0 h-10 px-2 border-b border-gray-300 bg-white">
          <span class="block text-sm font-medium bg-gray-500">BACKLOG</span>
        </div>
        <div class="flex flex-col px-2 pb-2 overflow-auto">
          <div v-for="error in backlog" :key="error.index">
            <div class="flex flex-row px-2 pb-2 overflow-auto">
              <div class="border border-black-600 text-center w-10">{{ error.code }}</div>
              <div class="border border-black-600 text-center w-96">{{ error.text }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists"
      );
      return {
        resolved,
        unresolved,
        backlog
      };
    } catch (error) {
      console.log(
        `Couldn't get error lists:\n${error}\nDid you start the API?`
      );
      console.log(
        "HINT: You can comment out the full `asyncData` method and work with mocked data for UI/UX development, if you want to."
      );
    }
  },
  data() {
    return {
      resolved: [],
      unresolved: [],
      backlog: []
    };
  }
};
</script>
