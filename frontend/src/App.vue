<template>
  <div id="app">
    <h1>Search ICD-10 Codes</h1>
    <input
      v-model="searchQuery"
      @input="debouncedSearch"
      type="text"
      placeholder="Search ICD codes or descriptions"
    />

    <h2>Results:</h2>
    <table v-if="icdCodes.length">
      <thead>
        <tr>
          <th>Code</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="code in icdCodes" :key="code.id">
          <td>{{ code.code }}</td>
          <td>{{ code.description }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No results found.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      searchQuery: "",
      icdCodes: [],
      debounceTimer: null, // Store the debounce timer
    };
  },
  created() {
    // Fetch all ICD codes initially when the app is loaded
    this.fetchAllICDCodes();
  },
  methods: {
    // Function to fetch all ICD codes
    async fetchAllICDCodes() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/icd_10_cm`);
        this.icdCodes = response.data;
      } catch (error) {
        console.error("Error fetching ICD codes:", error);
      }
    },
    // Function to search ICD codes based on user input
    async searchICDCodes() {
      const searchQuery = this.searchQuery.trim();

      if (!searchQuery) {
        // If the search query is empty, fetch all codes again
        this.fetchAllICDCodes();
      } else {
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/icd_10_cm?search=${encodeURIComponent(searchQuery)}`
          );
          this.icdCodes = response.data;
        } catch (error) {
          console.error("Error searching ICD codes:", error);
        }
      }
    },
    // Debounced search handler
    debouncedSearch() {
      // Clear the previous timer
      clearTimeout(this.debounceTimer);

      // Set a new timer to call searchICDCodes after 500ms delay
      this.debounceTimer = setTimeout(() => {
        this.searchICDCodes();
      }, 500); // Adjust the delay time as necessary
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
}

input {
  padding: 10px;
  width: 300px;
  margin-bottom: 20px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

table {
  width: 80%;
  max-width: 900px;
  border-collapse: collapse;
  margin: 0 auto;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

p {
  font-size: 18px;
  color: #666;
  margin-top: 20px;
}
</style>
