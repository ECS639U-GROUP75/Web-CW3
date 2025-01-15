<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
  <div class="h3">
    {{ title }}
  </div>
  <div class="content">
    <div class="Banner-section blue-color ">
      <div id="banner-image"></div>
      <div id="banner-lower-section" class="hobby-title">
        <h4 class="blue-color">{{ username }}</h4>
        <button id="edit-button" @click="openProfileEditModal"><i class="fa-solid fa-pen"></i> Edit</button>
      </div>
    </div>
    <div class="bottom-section">
      <div>
        <div id="Details_section" class="Table">
          <h4 class="blue-color">Details</h4>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-user"></i></b> : {{ name }}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-envelope"></i></b> : {{ email }}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-pen-nib"></i></b> : {{ bio }}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-calendar-days"></i></b> : {{ dob }}</div>
        </div>
      </div>
      <div id="Hobbies_section" class="Table full-width-table">
        <div class="hobby-title">
          <h4 class="blue-color">Hobbies</h4>
          <button id="add-button" @click="openHobbiesAddModal"><i class="fa-solid fa-plus"></i> Add</button>
        </div>
        <div class="Table-Row blue-color " v-for="hobby in hobbies" :key="hobby">
          {{ hobby }}
          <div>
            <button>
              <i class="fa-solid fa-dumpster"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL TEMPLATE FOR PROFILE EDIT -->
  <div class="modal fade" id="ProfileEditModal" aria-labelledby="ProfileEditModal" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1>Edit Profile</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div>
            <label for="username">Username</label>
            <input class="form-control" type="text" id="username" v-model="username" />
          </div>
          <div>
            <label for="email">Email</label>
            <input class="form-control" type="email" id="email" v-model="email" />
          </div>
          <div>
            <label for="bio">Bio</label>
            <textarea class="form-control" id="bio" v-model="bio"></textarea>
          </div>
          <div>
            <label for="dob">Date of Birth</label>
            <input class="form-control" type="date" id="dob" v-model="dob" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="saveProfileEditModal">Save changes</button>
          <button type="button" class="btn btn-secondary" @click="closeProfileEditModal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL TEMPLATE FOR HOBBY ADD -->
  <div class="modal fade" id="HobbyAddModal" aria-labelledby="HobbyAddModal" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1>Add Hobby</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="hobby-name">Hobby Name</label>
            <input 
              type="text" 
              id="hobby-name" 
              class="form-control" 
              v-model="newHobby"
              :class="{'is-invalid': addHobbyError}"
            />
            <div class="invalid-feedback" v-if="addHobbyError">
              {{ addHobbyError }}
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="saveAddHobbyModal"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Adding...' : 'Add Hobby' }}
          </button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL TEMPLATE FOR HOBBY EDIT -->
  <div class="modal fade" id="HobbyEditModal" aria-labelledby="HobbyEditModal" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1>Edit Hobby</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div>
            <label for="hobby-name">Hobby Name</label>
            <input type="text" id="hobby-name" v-model="selectedHobby" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="saveEditHobbyModal">Save changes</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useUserStore } from '../stores/userStore';
import 'bootstrap';
import * as bootstrap from 'bootstrap';
import { getCsrfToken } from '../utils/auth.ts';

export default defineComponent({
  inheritAttrs: false,
  setup() {
    const userStore = useUserStore();
    const title = ref("Profile");
    const username = ref("");
    const name = ref("");
    const email = ref("");
    const bio = ref("");
    const dob = ref("");
    const hobbies = ref<string[]>([]);
    const selectedHobby = ref("");
    const newHobby = ref("");
    const addHobbyError = ref("");
    const isSubmitting = ref(false);
    var temp_username = "";
    var temp_email = "";
    var temp_bio = "";
    var temp_dob = "";

    const fetchUserProfile = async () => {
      try {
        const response = await fetch('/api/profile/');
        if (!response.ok) {
          throw new Error('Failed to fetch user profile');
        }
        const data = await response.json();
        username.value = data.username;
        name.value  = data.first_name + " " + data.last_name;
        email.value = data.email;
        bio.value = data.bio;
        dob.value = data.date_of_birth;
        hobbies.value = data.hobbies;
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };
    const closeProfileEditModal = () => {
      username.value = temp_username;
      email.value = temp_email;
      bio.value = temp_bio;
      dob.value = temp_dob;
      temp_username = "";
      temp_email = "";
      temp_bio = "";
      temp_dob = "";
      const modal = bootstrap.Modal.getInstance(document.getElementById('ProfileEditModal'));
      modal.hide();
    };
    
    const openProfileEditModal = () => {
      temp_username = username.value;
      temp_email = email.value;
      temp_bio = bio.value;
      temp_dob = dob.value;
      const modal = new bootstrap.Modal(document.getElementById('ProfileEditModal'));
      modal.show();
    };
    const saveProfileEditModal = async () => {
      try {
        const csrfToken = await getCsrfToken();
        const modal = bootstrap.Modal.getInstance(document.getElementById('ProfileEditModal'));
        const response = await fetch('/api/update-profile/', {
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
          },
          credentials: 'include',
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            bio: bio.value,
            dob: dob.value,
          }),
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to update profile');
        }

        // Update was successful; fetch the updated profile to reflect changes
        const data = await response.json();
        username.value = data.username;
        email.value = data.email;
        bio.value = data.bio;
        dob.value = data.date_of_birth;
        
        
        modal.hide();
        
      } catch (error) {
        alert(`Failed to save profile: ${error.message}`);
      }
    };

    const openEditHobbyModal = (hobby) => {
      selectedHobby.value = hobby;
      const modal = new bootstrap.Modal(document.getElementById('HobbyEditModal'));
      modal.show();
    };

    const saveEditHobbyModal = () => {
      console.log("Saving hobby:", selectedHobby.value);
      const modal = bootstrap.Modal.getInstance(document.getElementById('HobbyEditModal'));
      modal.hide();
    };

    const openHobbiesAddModal = () => {
      const modal = new bootstrap.Modal(document.getElementById('HobbyAddModal'));
      modal.show();
    };
    const saveAddHobbyModal = async () => {
      if (!newHobby.value.trim()) {
        addHobbyError.value = "Hobby name cannot be empty";
        return;
      }

      if (hobbies.value.includes(newHobby.value.trim())) {
        addHobbyError.value = "You already have this hobby";
        return;
      }

      isSubmitting.value = true;
      addHobbyError.value = "";

      try {
        const csrfToken = await getCsrfToken();
        const response = await fetch('/api/add-hobby/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({
            name: newHobby.value.trim()
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to add hobby');
        }

        const data = await response.json();
        hobbies.value.push(newHobby.value.trim());
        newHobby.value = "";
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('HobbyAddModal'));
        modal?.hide();

      } catch (error: any) {
        addHobbyError.value = error.message;
      } finally {
        isSubmitting.value = false;
      }
    };

    onMounted(() => {
      fetchUserProfile();
    });

    return {
      title,
      username,
      name,
      email,
      bio,
      dob,
      hobbies,
      selectedHobby,
      newHobby,
      addHobbyError,
      isSubmitting,
      openProfileEditModal,
      saveProfileEditModal,
      openEditHobbyModal,
      saveEditHobbyModal,
      openHobbiesAddModal,
      saveAddHobbyModal,
      closeProfileEditModal
    };
  }
});
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
  display: grid;
  grid-template-columns: 35% 1% 64%;
  grid-template-areas: 
  'Details_section . Hobbies_section'
  ;
  max-width: 100%;
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
#Hobbies_section
{
  grid-area: Hobbies_section;
}
#Details_section
{
  grid-area: Details_section;
}
.Details-item
{
  padding: 1rem;
  border-bottom: 1pt solid #0a53be;
  margin-left: 1rem;
  margin-right: 1rem;
  white-space: nowrap;
  overflow: hidden;
  word-break: break-word;
  text-overflow: ellipsis;
}
h4
{
  padding: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  word-break: break-word;
  text-overflow: ellipsis;
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
#add-button, #edit-button
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