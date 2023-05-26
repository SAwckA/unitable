import Main from "@/pages/Main.vue";
import JournalList from "@/pages/JournalList.vue";
import Profile from "@/pages/Profile.vue";
import Auth from "@/pages/Auth.vue";
import {createRouter, createWebHistory} from "vue-router";
import Register from "@/pages/Register.vue";
import JournalCreate from "@/pages/JournalCreate.vue";
import Journal from "@/pages/Journal.vue";
import FindJournals from "@/pages/FindJournals.vue";

const routes = [
    {
        path: '/',
        component: Main
    },
    {
        path: '/auth',
        component: Auth
    },
    {
        path: '/register',
        component: Register
    },
    {
        path: '/profile',
        component: Profile,
    },
    {
        path: '/journals/my',
        component: JournalList
    },
    {
        path: '/journals/find',
        component: FindJournals
    },
    {
        path: '/journal/create',
        component: JournalCreate
    },
    {
        path: '/journal/:journal_id',
        component: Journal
    }
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
});

export default router