import { createFileRoute } from "@tanstack/react-router";
import { QuestionnaireFlow } from "@/components/QuestionnaireFlow";
import { ownerQuestions } from "@/lib/questionnaires";

export const Route = createFileRoute("/owner")({
  head: () => ({
    meta: [
      { title: "Pilot program — Property Owner · RentShield" },
      {
        name: "description",
        content: "Reduce vacancy and tenant risk. Answer 12 quick questions.",
      },
    ],
  }),
  component: OwnerFlow,
});

function OwnerFlow() {
  return (
    <QuestionnaireFlow
      userType="owner"
      questions={ownerQuestions}
      resultTitle="Your property may qualify for insured deposit reduction"
      resultBullets={[
        "Accept lower deposits without increasing your risk",
        "Damages and rent loss covered up to ₹2,00,000",
        "Requires move-in and move-out inspection photos",
        "Pilot includes free tenant verification scoring",
      ]}
      ctaLabel="Join Pilot Program"
    />
  );
}
