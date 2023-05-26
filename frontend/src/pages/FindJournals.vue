<template>
    <Header></Header>
    <div class="container" >
      <div class="container__name">
          <h1>Поиск журналов</h1>
      </div>
        <input v-model="query" @input="inputQuery" class="queryInput" placeholder="Введите название журнала">
      <div class="journals" >
          <div @click="openJournal(journal.id)" v-for="journal in journals" class="journal">
              <a>
              <span>
                  {{ journal.groupName }}
              </span>
              </a>
              <a v-if="journal.owner === null" class="owner">

              </a>
              <a v-else class="owner">
                  <span>{{ journal.owner.username }}</span>
                  <span>{{ journal.owner.email }}</span>
              </a>
          </div>
      </div>
    </div>
</template>

<script>
import Header from "@/components/Header.vue";
import axios from "axios";
import router from "@/router";

export default {
    name: "FindJournals",
    components: {Header},
    data(){
        return {
            query: '',
            journals: {

            },
            update: 0
        }
    },
    methods: {
        async inputQuery(e) {
            this.update++
            await this.getJournalList()
        },
        async getJournalList() {
            try {
                const resp = await axios.get('/api/journals',
                    {params: {
                            limit: 100,
                            group_name: this.query
                        }})
                this.journals = resp.data
            } catch (e) {

            } finally {

            }
        },
        openJournal(journalId) {
            router.push({'path': `/journal/${journalId}`})
        },
        openCreate(){
            router.push({'path': '/journal/create'})
        }
    },
    mounted() {
        this.getJournalList()
    }

}
</script>

<style scoped>
.container {
    max-width: 1440px;
    margin: auto;
}
.container__name {
    margin-top: 5rem;
    width: 100%;
}

.container__name h1 {
    text-align: center;
}

.journals {
    margin: auto;
    max-width: 1440px;
    min-width: 1440px;
    display: flex;
    justify-content: left;
    align-content: space-between;
    flex-flow: row wrap;
}

.journal {
    margin-top: 25px;
    margin-right: 2.5%;
    margin-left: 2.5%;
    box-shadow:  0px 7px 29px 0px rgba(100, 100, 111, 0.2) ;
    min-width: 20%;
    /*max-height: 10vh;*/
    padding: 20px;
    border-radius: 0.5rem;
    transition: 175ms;
    cursor: pointer;
}

.journal img {
    max-width: 50px;
    margin: auto;
}

.journal .create{
    display: block;
    width: 100%;
    text-align: center;
}

.journal:nth-child(4) {
    page-break-after: always;

}

.journal:hover {
    background-color: #eaeaea;
    transition: 175ms;
}
.journal:hover .owner {
    background-color: var(--button-color);
    transition: 175ms;
}

.owner {
    display: flex;
    flex-direction: column;
    background-color: var(--primary-color);
    color: white;
    padding: 10px;
    border-radius: 3px;
    box-shadow:  var(--box-shadow-default);
    transition: 175ms;
}

span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

input {
    border: 0;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    padding: 10px 25px;
    box-shadow: var(--box-shadow-default);
    margin-left: 2.5%
}

input:focus {
    color: #212529;
    background-color: #fff;
    border-color: var(--primary-color);
    outline: 0;
    box-shadow: var(--box-shadow-default);
}
</style>