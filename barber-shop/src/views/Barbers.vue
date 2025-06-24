<template>
  <div>
    <h2>Barbers</h2>

    <form @submit.prevent="addBarber">
      <label class="floating-label">
      <span>First Name</span>
      <input v-model="newBarber.first_name" placeholder="First Name" required />
      </label>
      <label class="floating-label">
      <span>Last Name</span>
      <input v-model="newBarber.last_name" placeholder="Last Name" required />
      </label>
      <label class="floating-label">
      <span>Age</span>
      <input v-model.number="newBarber.age" placeholder="Age" required />
      </label>
      <label class="floating-label">
      <span>address</span>
      <input v-model="newBarber.address" placeholder="Address" required />
      </label>
      <button class="btn btn-primary" type="submit">Add Barber</button>
    </form>

    <!-- <ul v-if="barbers.length">
      <li v-for="barber in barbers" :key="barber.id">
        {{ barber.first_name }} {{ barber.last_name }} - Age: {{ barber.age }}, Address: {{ barber.address }}
      </li>
    </ul> -->
<ul v-if="barbers.length" class="space-y-4">
  <li
    v-for="barber in barbers"
    :key="barber.id"
    class="card bg-base-100 shadow-md border border-base-200"
  >
    <div class="card-body p-4">
      <h2 class="card-title">
        {{ barber.first_name }} {{ barber.last_name }}
        <span class="badge badge-secondary ml-2">Age {{ barber.age }}</span>
      </h2>
      <p class="text-sm text-base-content/70">
        Address: {{ barber.address }}
      </p>
    </div>
  </li>
</ul>
    <p v-else>No barbers found.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Barbers",
  data() {
    return {
      barbers: [],
      newBarber: {
        first_name: "",
        last_name: "",
        age: null,
        address: ""
      },
    };
  },
  mounted() {
    this.fetchBarbers();
  },
  methods: {
    async fetchBarbers() {
      try {
        const res = await axios.get("http://localhost:8000/barbers");
        this.barbers = res.data;
      } catch (err) {
        console.error("Failed to fetch barbers:", err);
      }
    },
    async addBarber() {
      try {
        const res = await axios.post("http://localhost:8000/barbers", this.newBarber);
        this.barbers.push(res.data);
        // Reset form
        this.newBarber = {
          first_name: "",
          last_name: "",
          age: null,
          address: ""
        };
      } catch (err) {
        console.error("Failed to add barber:", err);
      }
    }
  }
};
</script>

<style scoped>
form {
  margin-bottom: 20px;
}

input {
  margin: 5px;
}
</style>
