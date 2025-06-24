<template>
  <div id="app">
    <nav class="navbar">
      <a class="btn btn-ghost text-xl">Barber Shop</a>
        <div class="navbar-center">
          <ul class="menu menu-horizontal lg:flex">
        <li><router-link to="/">Home</router-link></li> 
        <li><router-link to="/barbers">Barbers</router-link> </li>
        <li><router-link to="/hairstyles">Hairstyles</router-link> </li>
        <li><router-link to="/examples">Examples</router-link></li>
          </ul>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
nav {
  margin-bottom: 20px;
}
</style>

