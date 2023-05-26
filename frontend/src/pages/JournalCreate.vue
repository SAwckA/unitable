<template>
  <Header></Header>
  <div class="container">
      <form @submit.prevent>
          <input v-model="groupName" class="groupName" placeholder="Название журнала/группы">

          <div v-for="_student in studentList" class="students">
              <div class="student">
                  <span>{{ _student.fullName }}</span>
              </div>
          </div>

          <input v-model="newStudent" class="student__add" placeholder="ФИО студента">
          <button @click="addStudent">Добавить</button>
          <button @click="createJournal">Создать журнал</button>
      </form>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import axios from "axios";
import router from "@/router";

export default {
    name: "JournalCreate",
    components: {Header},
    data() {
        return {
            groupName: '',
            newStudent: '',
            studentList: []
        }
    },
    methods: {
        addStudent() {
            this.studentList.push({'fullName': this.newStudent})
            this.newStudent = ''
        },

        async createJournal() {
            try {
                const journal = await axios.post('/api/journal', {
                    'groupName': this.groupName
                })
                const journal_id = journal.data.id

                await axios.post(`/api/journal/${journal_id}/students`, this.studentList)

                await router.push({path:`/journal/${journal_id}`})

            } catch (e) {

            } finally {

            }
        }
    }
}
</script>

<style scoped>

</style>