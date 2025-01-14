<template>

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">


  <div class="h3">
    {{ title }}
  </div>
  <div class="content">
    <div class="Banner-section blue-color ">
      <div id="banner-image">
        
      </div>
      <div id="banner-lower-section" class="hobby-title">
        <h4 class="blue-color">Username</h4>
        <button id="add-button"><i class="fa-solid fa-pen"></i> Edit</button>
      </div>
    </div>
    <div class="bottom-section">
      <div>
        <div class="Table">
          <h4 class="blue-color">Details</h4>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-user"></i></b> : {{name}}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-envelope"></i></b> : {{email}}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-pen-nib"></i></b> : {{Bio}}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-calendar-days"></i></b> : {{DOB}}</div>
        </div>
      </div>
      <div class="Table full-width-table">
        
        <div class="hobby-title">
          <h4 class="blue-color">Hobbies</h4>
          <button id="add-button"><i class="fa-solid fa-plus"></i> Add</button>
        </div>
        <div class="Table-Row blue-color " v-for="hobby in Hobbies">
          {{hobby}}
          <div>
            <button>
              <i class="fa-solid fa-pen"></i>
            </button>
            <button>
              <i class="fa-solid fa-dumpster"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    
  </div>
  
  
  
  
  
  <!-- MODAL TEMPLATE -->
  <div class="modal fade" id="HobbyEditModal"  aria-labelledby="HobbyEditModal" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1>Hobby (CHANGE WITH RESPECTIVE HOBBY)</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div>HOBBY NAME</div>
        </div>
      </div>
    </div>
  </div>
  
  
  
  
  
</template>




<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      title: "Profile",
      name: "Davide",
      email : "temp",
      Bio : "ggson, i am the best there is...",
      DOB : "random",
      Hobbies : ["HOBBY1","HOBBY2","HOBBY3","HOBBY4","HOBBY5","HOBBY6","HOBBY7"]
    }
  }
})
</script>




<style scoped>
.full-width-table
{
  width: 100%;
}
.hobby-title
{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.Banner-section
{
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 1rem;
}
.bottom-section
{
  display: flex;
  felx-direction: row;
  gap: 1rem;
}
.Table
{
  display: flex;
  flex-direction: column;
  border-radius: 0.5rem;
  background-color: white;
  padding: 1rem;
  
}
.Table-Row
{
  display: flex;
  flex-direction: row;
  padding: 1rem;
  margin-left: 1rem;
  margin-right: 1rem;
  justify-content: space-between;
  border-bottom: black 1pt solid;
}
.content
{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  background-color: #e5e5e5;
  border-radius: 0.5rem;
  padding: 1rem;
}
.Details-item
{
  padding: 1rem;
  border-bottom: 1pt solid #0a53be;
  margin-left: 1rem;
  margin-right: 1rem;
}
h4
{
  padding: 0.5rem;
}
.blue-color
{
  color: #0a53be;
}
#banner-image
{
  width: 100%;
  height: 10rem;
  border: solid 1pt #0a53be;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}
#add-button
{
  background-color: #0a53be;
  border-color: #0a53be;
  border-radius: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
  color: white;
}
#banner-lower-section
{
  padding: 0.5rem;
  padding-right: 1rem;
}
</style>