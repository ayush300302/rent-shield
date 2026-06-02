import { createFileRoute } from "@tanstack/react-router";
import { QuestionnaireFlow } from "@/components/QuestionnaireFlow";
import { renterQuestions } from "@/lib/questionnaires";

export const Route = createFileRoute("/renter")({
  head: () => ({
    meta: [
      { title: "Check eligibility — Renter · RentShield" },
      {
        name: "description",
        content: "Reduce your upfront rental deposit. Answer 8 quick questions.",
      },
    ],
  }),
  component: RenterFlow,
});

function RenterFlow() {
  return (
    <QuestionnaireFlow
      userType="renter"
      questions={renterQuestions}
      resultTitle="You may qualify for deposit replacement coverage up to ₹2,00,000"
      resultBullets={[
        "Reduce upfront deposit from 6 months to 1 month",
        "Coverage requires move-in and move-out inspection photos",
        "Priority access to RentShield beta partner landlords",
      ]}
      ctaLabel="Join Early Access"
    />
  );
}
