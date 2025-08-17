import { useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";

export default function CounterScreen() {
  const [count, setCount] = useState(0);

  return (
    <View style={styles.container}>
      <Text style={styles.number}>Contagem: {count}</Text>
      <Button title="➕ Incrementar" onPress={() => setCount(count + 1)} />
      <Button title="➖ Decrementar" onPress={() => setCount(count - 1)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  number: { fontSize: 30, marginBottom: 20 },
});