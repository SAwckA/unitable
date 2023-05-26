<template>
    <Header></Header>
    <div class="content__container">
        <section class="content">
            <h1>
                Landing (section 1)
            </h1>
        </section>
        <section class="content">
            <h1>
                Landing (section 2)
            </h1>
        </section>
    </div>
</template>

<script>
import Header from "@/components/Header.vue";
export default {
    name: "Main",
    components: {
        Header
    }
}
</script>

<style scoped>

.content__container {
    max-width: 1440px;
    min-width: 1440px;
    margin: auto;
}

.content {
    height: 100vh;
}
</style>