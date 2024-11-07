<template>
  <div id="app">
    <h1>Search ICD-10 Codes</h1>
    <input
      v-model="searchQuery"
      @input="searchICDCodes"
      type="text"
      placeholder="Search"
    />

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
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 40px; /* Adjusted top margin */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
}

input {
  padding: 10px;
  width: 300px; /* Set width of input field */
  margin-bottom: 20px; /* Space below the input */
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

table {
  width: 80%;
  max-width: 900px; /* Limit the table width */
  border-collapse: collapse;
  margin: 0 auto; /* Center the table horizontally */
}

th, td {
  border: 1px solid #ddd;
  padding: 12px 15px; /* Add padding for more spacious cells */
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
